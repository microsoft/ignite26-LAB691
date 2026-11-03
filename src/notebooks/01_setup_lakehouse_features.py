# Fabric notebook source
# This notebook prepares raw data and builds customer-level feature tables.

# %% [markdown]
# # 01 - Setup Lakehouse and Build Customer Features
#
# Expected Lakehouse files:
# - Files/raw/customers/customers.csv
# - Files/raw/orders/orders.parquet
# - Files/raw/feedback/*.txt
# - Files/raw/support/support_cases.json

# %%
from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark.conf.set("spark.sql.session.timeZone", "UTC")
run_date = F.current_date()

# %% [markdown]
# ## 1) Ingest customers and orders into Delta tables

# %%
customers_path = "Files/raw/customers/customers.csv"
orders_path = "Files/raw/orders/orders.parquet"
support_path = "Files/raw/support/support_cases.json"
feedback_path = "Files/raw/feedback/*.txt"

customers_df = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(customers_path)
    .withColumn("signup_date", F.to_date("signup_date"))
)

orders_df = (
    spark.read.parquet(orders_path)
    .withColumn("order_date", F.to_date("order_date"))
    .withColumn("amount", F.col("amount").cast("double"))
)

support_df = (
    spark.read.option("multiLine", True)
    .json(support_path)
    .withColumn("opened_date", F.to_date("opened_date"))
)

customers_df.write.mode("overwrite").format("delta").saveAsTable("customers")
orders_df.write.mode("overwrite").format("delta").saveAsTable("orders")
support_df.write.mode("overwrite").format("delta").saveAsTable("support_cases")

# %% [markdown]
# ## 2) Read feedback text and compute sentiment fallback
# If AI-powered Shortcut Transformation is enabled in your Fabric environment,
# use that output table instead and skip this fallback scoring.

# %%
feedback_raw = (
    spark.read.text(feedback_path)
    .withColumn("path", F.input_file_name())
    .withColumn("customer", F.regexp_extract("path", r"(CUST\d{4})\.txt$", 1))
    .withColumnRenamed("value", "comment")
)
feedback_raw.write.mode("overwrite").format("delta").saveAsTable("feedback_raw")

positive_words = [
    "excellent",
    "great",
    "useful",
    "value",
    "responsive",
    "easy",
]
negative_words = [
    "delay",
    "unresolved",
    "high",
    "difficult",
    "improvement",
    "bug",
]

def score_expr(words, sign=1):
    total = F.lit(0)
    for w in words:
        total = total + F.when(
            F.lower(F.col("comment")).contains(w), F.lit(sign)
        ).otherwise(F.lit(0))
    return total

feedback_sentiment = (
    feedback_raw.withColumn("sentiment_score", score_expr(positive_words, 1) + score_expr(negative_words, -1))
    .withColumn(
        "sentiment_label",
        F.when(F.col("sentiment_score") > 0, F.lit("Positive"))
        .when(F.col("sentiment_score") < 0, F.lit("Negative"))
        .otherwise(F.lit("Neutral")),
    )
)
feedback_sentiment.write.mode("overwrite").format("delta").saveAsTable("feedback_sentiment")

# %% [markdown]
# ## 3) Customer-level feature engineering

# %%
order_agg = (
    orders_df.groupBy("customer")
    .agg(
        F.sum("amount").alias("lifetime_value"),
        F.count("*").alias("order_count"),
        F.max("order_date").alias("last_order_date"),
        F.min("order_date").alias("first_order_date"),
    )
    .withColumn("days_since_last_purchase", F.datediff(F.current_date(), F.col("last_order_date")))
    .withColumn(
        "active_months",
        F.greatest(
            F.lit(1),
            F.months_between(F.current_date(), F.col("first_order_date")).cast("int"),
        ),
    )
    .withColumn("order_frequency_per_month", F.round(F.col("order_count") / F.col("active_months"), 3))
)

sent_agg = (
    feedback_sentiment.groupBy("customer")
    .agg(
        F.avg("sentiment_score").alias("average_sentiment"),
        F.max("comment").alias("sample_comment"),
    )
)

support_agg = (
    support_df.groupBy("customer")
    .agg(F.count("*").alias("support_case_count"))
)

customer_features = (
    customers_df.join(order_agg, "customer", "left")
    .join(sent_agg, "customer", "left")
    .join(support_agg, "customer", "left")
    .fillna({"average_sentiment": 0.0, "support_case_count": 0})
    .withColumn(
        "retention_risk",
        F.when(
            (F.col("days_since_last_purchase") > 120)
            & (F.col("order_frequency_per_month") < 0.75)
            & (F.col("average_sentiment") < 0),
            F.lit("High"),
        )
        .when(
            (F.col("days_since_last_purchase") > 60)
            | (F.col("average_sentiment") <= 0),
            F.lit("Medium"),
        )
        .otherwise(F.lit("Low")),
    )
)

customer_features.write.mode("overwrite").format("delta").saveAsTable("customer_features")

# %%
display(customer_features.orderBy(F.desc("lifetime_value")).limit(20))

