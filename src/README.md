# Source

This folder contains the notebooks and SQL used in the [attendee instructions](../instructions/README.md).

| File | Purpose | Workshop step |
| --- | --- | --- |
| [Lakehouse setup and customer features](./notebooks/01_setup_lakehouse_features.ipynb) | Loads the sample data into Delta tables and builds customer-level metrics with fallback sentiment scoring. | Step 4 |
| [Polars segmentation](./notebooks/02_polars_segmentation.ipynb) | Adds value and engagement tiers and writes `customer_segments`. | Step 5 |
| [Customer 360 SQL views](./customer_360_views.sql) | Creates reporting views for customer details, monthly sales, and retention summaries. | Step 6 |
| [Customer 360 notebook app](./notebooks/03_customer360_notebook_app.py) | Provides interactive exploration of existing customer, order, and feedback tables. | Step 7 |

Import the notebooks into Fabric using **Python (PySpark)** and attach the lab Lakehouse as the default. Run the SQL statements separately in its **SQL analytics endpoint**. Follow the attendee instructions for prerequisites, execution order, and overwrite warnings.
