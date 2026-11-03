# Fabric notebook source
# This notebook uses Polars to build the customer_segments Delta table.

# %% [markdown]
# # 02 - Polars Segmentation
# Run with Python (PySpark) and the default Lakehouse containing customer_features.

# %%
# If needed in your Fabric runtime:
# %pip install polars

import polars as pl

# %% [markdown]
# ## 1) Load customer feature table and segment with Polars

# %%
features_pd = spark.table("customer_features").toPandas()
features = pl.from_pandas(features_pd)

ltv_q = features.select(
    pl.col("lifetime_value").quantile(0.33).alias("q33"),
    pl.col("lifetime_value").quantile(0.66).alias("q66"),
).to_dicts()[0]

q33 = float(ltv_q["q33"])
q66 = float(ltv_q["q66"])

segmented = (
    features.with_columns(
        pl.when(pl.col("lifetime_value") < q33)
        .then(pl.lit("Low"))
        .when(pl.col("lifetime_value") < q66)
        .then(pl.lit("Medium"))
        .otherwise(pl.lit("High"))
        .alias("value_tier"),
        pl.when(
            (pl.col("days_since_last_purchase") > 120)
            | (pl.col("order_frequency_per_month") < 0.5)
        )
        .then(pl.lit("At Risk"))
        .when(
            (pl.col("days_since_last_purchase") > 60)
            | (pl.col("order_frequency_per_month") < 1.0)
        )
        .then(pl.lit("Watch"))
        .otherwise(pl.lit("Healthy"))
        .alias("engagement_tier"),
    )
)

spark.createDataFrame(segmented.to_pandas()).write.mode("overwrite").format("delta").saveAsTable("customer_segments")

# %%
display(spark.table("customer_segments").groupBy("segment", "value_tier", "engagement_tier").count())
