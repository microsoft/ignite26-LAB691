# Fabric notebook source
# This notebook builds an interactive app from existing Customer 360 tables.

# %% [markdown]
# # 03 - Customer 360 Notebook App
# Run with Python (PySpark) after 02_polars_segmentation.py.
# Set the default Lakehouse containing customer_segments, customers, orders,
# and feedback_sentiment.

# %%
from pyspark.sql import functions as F
import ipywidgets as widgets
from IPython.display import display, clear_output

# %% [markdown]
# ## 1) Build notebook app controls

# %%
segments = [r["segment"] for r in spark.table("customers").select("segment").distinct().orderBy("segment").collect()]
customers = [r["customer"] for r in spark.table("customers").select("customer").distinct().orderBy("customer").collect()]

segment_dropdown = widgets.Dropdown(
    options=["All"] + segments,
    value="All",
    description="Segment:",
)
customer_dropdown = widgets.Dropdown(
    options=["All"] + customers,
    value="All",
    description="Customer:",
)
run_button = widgets.Button(description="Refresh", button_style="primary")
output = widgets.Output()

ui = widgets.HBox([segment_dropdown, customer_dropdown, run_button])
display(ui, output)


def render_view(_):
    with output:
        clear_output(wait=True)

        seg = segment_dropdown.value
        cust = customer_dropdown.value

        query = spark.table("customer_segments")
        if seg != "All":
            query = query.filter(F.col("segment") == seg)
        if cust != "All":
            query = query.filter(F.col("customer") == cust)

        selected = query.orderBy(F.desc("lifetime_value"))
        print("Customer overview")
        display(selected.select(
            "customer",
            "segment",
            "location",
            "lifetime_value",
            "order_frequency_per_month",
            "days_since_last_purchase",
            "average_sentiment",
            "support_case_count",
            "retention_risk",
            "value_tier",
            "engagement_tier",
        ))

        selected_customers = [r["customer"] for r in selected.select("customer").limit(25).collect()]
        if not selected_customers:
            print("No records for selected filters.")
            return

        orders = (
            spark.table("orders")
            .filter(F.col("customer").isin(selected_customers))
            .orderBy(F.desc("order_date"))
        )
        print("Recent transactions")
        display(orders.limit(100))

        feedback = (
            spark.table("feedback_sentiment")
            .filter(F.col("customer").isin(selected_customers))
            .select("customer", "sentiment_label", "sentiment_score", "comment")
        )
        print("Voice of customer")
        display(feedback.limit(100))


run_button.on_click(render_view)
render_view(None)
