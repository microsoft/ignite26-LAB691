# LAB691: Build an AI-ready data foundation with Microsoft OneLake

## Welcome to Your Lab Environment

To begin, log into the virtual machine using the following credentials: +++@lab.VirtualMachine(Win11-Pro-Base).Password+++


## Audience and objective

In this workshop, you will combine customer profile data, order transactions, and unstructured customer feedback to build a **Customer 360** view that highlights:

- customer value
- engagement
- sentiment
- retention risk

You will leave with:
- curated Delta tables in a Lakehouse
- a customer-level feature table
- segmented customers using Polars
- a Power BI report model
- a notebook app for customer drill-down

## Prerequisites

- Open the browser and download a local copy of the workshop from `https://github.com/microsoft/ignite26-LAB691/archive/refs/heads/main.zip`
- From the Downloads folder, unzip the lab onto the desktop so it's easier to find

## Lab flow and timing (75 min)

1. **0-10 min**: Setup, upload data, and create Lakehouse folders  
2. **10-20 min**: Ingest profile data and create shortcut for orders  
3. **20-35 min**: Transform feedback with AI-powered shortcuts (preview)  
4. **35-55 min**: Spark feature engineering for customer-level metrics  
5. **55-65 min**: Polars segmentation  
6. **65-75 min**: Power BI Customer 360 report + notebook app

---

## Log in to Microsoft Fabric

To start the lab:
1. Open up browser
2. With the address bar selected, click here: +++https://app.fabric.microsoft.com+++
3. From the intstructions pane, swtich to the Resources tab
4. Click Username to insert the email
5. Click TAP to insert the temp password
6. Switch back to the Instructions tab

## Step 0 - Create Workspace and Locate the included sample data

### Create a workspace
1. Select **Workspaces** from the left nav
2. Click **+ New Workspace** button
3. Give your workspace a name and scroll down ensuring Workspace Type is set to *Fabric*
4. Click **Apply** to create your new workspace

### Locate sample data

The sample data is included in a local folder on your desktop named *ignite26-LAB691* under the subfolder */data/raw*

Data included:
- [Customer profiles](https://github.com/microsoft/ignite26-LAB691/tree/main/data/raw/customers.csv)
- [Orders](https://github.com/microsoft/ignite26-LAB691/tree/main/data/raw/orders.parquet)
- [Customer feedback text files](https://github.com/microsoft/ignite26-LAB691/tree/main/data/raw/feedback/)
- [Support cases](https://github.com/microsoft/ignite26-LAB691/tree/main/data/raw/support_cases.json)

Review the [dataset overview](https://github.com/microsoft/ignite26-LAB691/tree/main/data/README.md) for formats, fields, and relationships. Keep these files available for upload in Step 1.

---

## Step 1 - Create Lakehouse structure

1. In Fabric, select the new workspace you created (if not already selected) from the left nav.
2. Create a new **Lakehouse** named `lh_customer360`.
3. Under Files, create subfolders:
   - `raw/customers`
   - `raw/orders`
   - `raw/feedback`
   - `raw/support`
4. Upload these local files:
   - data/raw/customers.csv -> Files/raw/customers/
   - data/raw/orders.parquet -> Files/raw/orders/
   - all files from data/raw/feedback/ -> Files/raw/feedback/
   - data/raw/support_cases.json -> Files/raw/support/

---

## Step 2 - Transform feedback with AI-powered shortcuts

### Create sentiment analysis and PII redaction transformations

Use AI-powered shortcut transformations to turn the customer feedback text files into queryable Delta tables without first running a notebook. Follow [Shortcut transformations (AI-powered) (Microsoft Learn)](https://learn.microsoft.com/en-us/fabric/onelake/shortcuts/transformations-ai).

**Before you start:**

- This feature is in **public preview**. You need a Fabric capacity or trial supporting Lakehouse workloads, a **Contributor** or higher workspace role, and a [supported region](https://learn.microsoft.com/en-us/azure/ai-services/language-service/concepts/regional-support).
- The input must be a folder of `.txt` files. Use the feedback folder uploaded in Step 1, `Files/raw/feedback`, as the OneLake source.
- If the AI transformation options are unavailable, continue with the notebook in Step 4 as a fallback.

#### Create the sentiment analysis transformation

1. Open `lh_customer360`. In **Explorer**, start shortcut creation in **Tables**. Right-click **dbo** and select **New table shortcut**; otherwise use **New shortcut**. Learn more in [table shortcut creation guidance](https://learn.microsoft.com/en-us/fabric/onelake/shortcuts/transformations#create-a-table-shortcut-with-data-transformation).
2. Choose **Microsoft OneLake** under **Internal sources**. Select the Lakehouse containing the uploaded feedback files and select **Next**.
3. Keep **Pass-through** as the connection method, then expand **Files > raw**, select the physical **feedback** folder, and select **Next**. Use the folder containing the `.txt` files, not an individual file or a folder containing only other shortcuts.
4. During shortcut creation, choose the AI-powered **Sentiment analysis** transformation. This classifies the feedback as positive, negative, or neutral.
5. Review **Connect to access data**. It is created by default for new transformations. Click *Next* to continue.
6. Review the destination and set the shortcut/output table name to `feedback_ai_sentiment`, keeping it separate from the optional notebook's tables. Select **Create**.
7. Wait for the transformation output, then open the resulting Delta table under **Tables** and inspect its columns and sentiment results. If you see *Unidentified* or *Unable to identify these objects as tables* error, select the ellipsis under *Tables* and hit **Refresh**.  You can check progress of the transform under *Notifications* (bell icon) at top of your Fabric window.

---

## Step 3 - Build customer-level features in Spark

In this step, you will use a Spark notebook to combine customer profiles, orders, feedback, and support cases into a customer-level feature table with measures of value, engagement, sentiment, and retention risk. Bringing these signals together creates a reusable foundation for customer segmentation and reporting, helping you identify valuable customers and those who may need attention.

### What to expect from this notebook

The notebook computes these features:

- **lifetime_value** (sum of order amount)
- **order_frequency_per_month**
- **days_since_last_purchase**
- **average_sentiment**
- **support_case_count**

Output table:

- `customer_features`

Retention risk heuristic is also produced:

- High risk: low order frequency + negative sentiment + high recency
- Medium/Low risk for remaining customers

Furthermore, this notebook creates:

- `customers` Delta table
- `orders` Delta table
- `feedback_raw` and `feedback_sentiment` Delta tables
- `support_cases` Delta table

The notebook includes fallback lexicon sentiment. Its `feedback_sentiment` table is separate from `feedback_ai_sentiment`; running it is not required to create or inspect the AI-powered transformation outputs.
### Preparing tables
#### Import and configure the notebook

1. Open the Fabric workspace containing `lh_customer360`.
2. In the workspace toolbar, open the notebook import option **--> | Import** and select **Notebook**
3. Browse to your local repository's `src/notebooks` folder and select `01_setup_lakehouse_features.ipynb`. Complete the import and open the new notebook item. Learn more [Import existing notebooks (Microsoft Learn)](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook#import-existing-notebooks).
4. Choose the notebook experience based on the code:
   - **For this notebook, use Spark with Python (PySpark).** It imports `pyspark.sql`, uses the `spark` session, and writes Delta tables with Spark. Do **not** switch it to the non-Spark Python experience.
5. In the notebook's Lakehouse explorer, select **Add data items**, choose **From OneLake Catalog**
6. Select the existing `lh_customer360` Lakehouse, and add it. Pin it as the **default Lakehouse** so the notebook's relative `Files/...` paths resolve correctly. If a session is already running when you change the default Lakehouse, restart it.
7. Review the imported code and confirm that the customer, order, feedback, and support files from Step 1 are present.
8. Select and run each cell and wait for the Spark execution to finish. Check for cell errors, then refresh the Lakehouse's **Tables** area and confirm the output tables are available, including `customer_features`.

---

## Step 4 - Segment with Polars

Use [02_polars_segmentation.py](https://github.com/microsoft/ignite26-LAB691/tree/main/src/notebooks/02_polars_segmentation.ipynb) to turn the customer features from Step 4 into actionable customer groups, helping you identify high-value customers and customers whose purchasing activity may need attention. This notebook only builds segmentation; the separate interactive app notebook is used in Step 7.

### What the notebook does

1. Reads the `customer_features` Delta table with Spark, converts it to a pandas DataFrame, and then loads it into Polars for segmentation.
2. Adds a **value tier** based on lifetime value (LTV): **Low** below the 33rd-percentile cutoff, **Medium** from that cutoff to below the 66th-percentile cutoff, and **High** at or above the upper cutoff. These are relative tiers within this dataset, not fixed spending thresholds.
3. Adds an **engagement tier** using purchase recency and frequency:
   - **At Risk**: More than 120 days since the last purchase **or** fewer than 0.5 orders per month.
   - **Watch**: For customers not already At Risk, more than 60 days since the last purchase **or** fewer than 1 order per month.
   - **Healthy**: All remaining customers.
4. Writes the enriched data back to the Lakehouse as the `customer_segments` Delta table and displays customer counts grouped by segment, value tier, and engagement tier. The existing `retention_risk` feature from Step 4 remains separate from the new engagement tier.
Together, these tiers provide a reusable basis for reporting and prioritizing customer outreach. Step 7 uses this output to examine the underlying purchases and feedback in an interactive view.

### Import and run the notebook in Fabric

1. Complete Step 4 first. In `lh_customer360`, confirm that `customer_features` exists; this notebook reads that table.
2. Open the Fabric workspace containing that Lakehouse. In the workspace toolbar, select **Import notebook** (it may appear under **New** in your workspace layout).
3. Browse to your local repository's `src/notebooks` folder, select `02_polars_segmentation.ipynb`, and complete the import. Open the resulting notebook item. Learn more [Import existing notebooks (Microsoft Learn)](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook#import-existing-notebooks).
4. **Use the Spark notebook experience with Python (PySpark), not the non-Spark Python experience.** Although the segmentation uses Polars, this notebook calls `spark.table()` and `spark.createDataFrame()` and uses Spark to save the Delta table. Learn more [Use Python experience on Notebook (Microsoft Learn)](https://learn.microsoft.com/en-us/fabric/data-engineering/using-python-experience-on-notebook#how-to-access-a-python-notebook).
5. In the notebook's Lakehouse explorer, select **Add lakehouse**, choose the existing `lh_customer360`, and pin it as the **default Lakehouse**. Restart an already-running session if you change its default Lakehouse.
6. Review the code before running. It collects the feature table into driver memory for pandas and Polars, so this approach is intended for the small lab dataset rather than an arbitrarily large customer table. It also **overwrites** `customer_segments`; use your lab Lakehouse.
7. Run each of the cells one at a time. If the Polars import fails because the package is missing, uncomment the provided `%pip install polars` line, run that installation cell, and rerun the notebook.
8. Check that all cells finish successfully. Refresh the Lakehouse's **Tables** area and confirm that `customer_segments` exists and includes `value_tier` and `engagement_tier`. Review the displayed grouped customer counts.

---

## Step 5 - Power BI Customer 360 report

Use [customer_360_views.sql](https://github.com/microsoft/ignite26-LAB691/tree/main/src/customer_360_views.sql) to create a reusable SQL reporting layer over the Delta tables prepared in Steps 4 and 5. The views give Power BI consistent customer details and sales and retention summaries, so you do not need to repeat those queries in each report. They are the reporting layer used in this exercise, not a requirement for querying the underlying tables directly.

### What the SQL file does

The script uses `CREATE OR ALTER VIEW` to create or update three views:

| View | What it provides | Reporting use |
| --- | --- | --- |
| `vw_customer_360` | Customer attributes, lifetime value, order counts and frequency, purchase recency, sentiment, support case counts, retention risk, and value and engagement tiers from `customer_segments`. | Customer KPIs, segmentation, and drill-through details. |
| `vw_sales_monthly` | Order amounts summed by month, customer, and product from `orders`. Each month is represented by its first calendar day. | Monthly revenue trends and customer or product breakdowns. |
| `vw_retention_summary` | Customer counts and summed lifetime value grouped by customer segment and retention risk from `customer_segments`. | Comparing risk groups and the customer value associated with them. |

Views store query definitions, not separate copies of the data. The script does not change the source tables, and rerunning it updates the view definitions. Changes to the underlying tables are reflected when the views are queried after those changes are available in the SQL analytics endpoint.

### Create and verify the views

1. Open `lh_customer360` in Fabric and switch to its **SQL analytics endpoint**, by selecting it from the drop down in the top, right corner of the Fabric UI.
2. In the endpoint's Explorer, confirm that `customer_segments` and `orders` are visible under **Schemas > dbo > Tables**. If they have just been created, allow time for the endpoint to synchronize their metadata and refresh the Explorer. You need permission to create views in this endpoint.
3. Select **New SQL query** drop down (down arrow) from the main screen and choose **New SQL query (from file)**
4. Open the local repository file `https://github.com/microsoft/ignite26-LAB691/tree/main/src/customer_360_views.sql` in your editor. You will copy its SQL into the endpoint's query editor; you do not need to upload the file to Lakehouse **Files**.
5. To find and connect to the correct endpoint, return to your Fabric workspace and open `lh_customer360`. In the upper-right experience selector, switch from **Lakehouse** to **SQL analytics endpoint**. Alternatively, open the workspace item named `lh_customer360` whose type is **SQL analytics endpoint**, rather than the Lakehouse item. Fabric creates this endpoint automatically with the Lakehouse. Opening it in the browser uses your signed-in Fabric account; no separate server connection is needed for this exercise. Confirm that Explorer shows the expected tables before opening a query.
6. Select **New SQL query**. Copy the first statement, starting with `CREATE OR ALTER VIEW vw_customer_360` and ending with `FROM customer_segments cs;`, into the query editor and select **Run**.
7. In a separate query tab, copy and run the full `CREATE OR ALTER VIEW vw_sales_monthly` statement. Repeat in another tab for `vw_retention_summary`. Run each view definition separately: a `CREATE VIEW` statement must start its own query batch, so do not run all three statements together as a single batch.
8. If the source tables use a schema other than your default schema, qualify the table references in the copied SQL with the schema shown in Explorer, for example `dbo.customer_segments` or `dbo.orders` when they are under `dbo`. Resolve any missing-table or permission errors before continuing.
9. Refresh **Views** in Explorer and confirm that all three views appear. In a new query tab, run these checks, qualifying the view names with their schema if needed:

   ```sql
   SELECT TOP (10) * FROM vw_customer_360;
   SELECT TOP (10) * FROM vw_sales_monthly ORDER BY sales_month DESC;
   SELECT * FROM vw_retention_summary ORDER BY segment, retention_risk;
   ```

9. Confirm that the customer view includes the segmentation tiers, the sales view contains monthly revenue, and the retention view contains customer counts and lifetime-value totals by risk group.

### Use the views in Power BI

1. Use Power BI within the **Fabric portal** to create a semantic model from the SQL analytics endpoint and build a report. All the following steps happen in your browser; Power BI Desktop is not required.
2. Open your Fabric workspace and select the **SQL analytics endpoint** for `lh_customer360`, or open the Lakehouse and switch to **SQL analytics endpoint** using the experience selector. Confirm that the three reporting views appear in Explorer. Your account needs access to query the views and permission to create a semantic model in the destination workspace.
3. On the endpoint's ribbon, select **New semantic model**. Start from the SQL analytics endpoint, rather than creating a model directly from OneLake files. See [Create a Power BI semantic model in the Fabric portal (Microsoft Learn)](https://learn.microsoft.com/en-us/fabric/data-warehouse/create-semantic-model#create-a-new-power-bi-semantic-model-in-direct-lake-mode).
4. Enter a model name, such as `Customer 360`, and select the lab workspace as its destination. In the object selection, expand the schema and select `vw_customer_360` and `vw_sales_monthly`; optionally include `vw_retention_summary` for separate summary visuals. Select **Confirm**. If the views are missing, check the endpoint, refresh its metadata, and verify your permissions before proceeding.
5. Understand the connection mode: the endpoint-based creation workflow uses **Direct Lake on SQL**. SQL views are discovered through the endpoint but cannot be read as physical Delta tables, so queries against these views use **DirectQuery fallback**. Leave fallback enabled; a Direct Lake-only configuration would prevent these view queries from running. **Direct Lake on OneLake** does not offer this fallback and is not the connection to use for these SQL views. See [Direct Lake options (Microsoft Learn)](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview).
6. Open the model in the browser. If it does not open automatically, find the new semantic model in your workspace and select **Open data model** from its context menu. Create or verify an active **one-to-many** relationship from `vw_customer_360[customer]` to `vw_sales_monthly[customer]`, with **Single** cross-filter direction from customers to sales. Both keys should have the same data type, and the customer view must contain unique customer identifiers. Verify that `sales_month` is a date and revenue and lifetime value are numeric.
7. Confirm that the model is saved in the workspace. If queries report a connection or authentication error, open the semantic model's **Settings** and review **Gateway and cloud connections**, mapping an authorized cloud connection or signing in if prompted. The connection identity must have access to the endpoint's views. You do not need to publish a local Power BI file.
8. Select **New report** from the browser model editor, then save the report in your lab workspace. Add a simple customer-count or revenue visual first to verify that the model can query the views, then build a report with:
   - **Executive KPI cards**: customers, LTV, avg sentiment, high-risk count
   - **Segment matrix**: segment vs value_tier vs risk
   - **Trend chart**: monthly sales
   - **Customer detail page** with drill-through
   - **Map** by customer location

Use `vw_customer_360` and `vw_sales_monthly` for the customer and sales model. The optional `vw_retention_summary` view already contains grouped totals; use it for summary visuals without adding its totals to customer-level totals or treating it as a customer-detail table.

---

## Step 6 - Data app experience

Use [03_customer360_notebook_app.py](https://github.com/microsoft/ignite26-LAB691/tree/main/src/notebooks/03_customer360_notebook_app.py) to explore the existing Customer 360 tables as an interactive data app. The notebook creates interactive controls where users choose:

- a segment, and/or
- a specific customer

And immediately see:

- transaction history
- sentiment summary
- support case load
- retention indicator

### Import and run the app notebook

1. Complete Steps 4 and 5 first. Confirm that `customer_segments`, `customers`, `orders`, and `feedback_sentiment` exist in `lh_customer360`.
2. In the Fabric workspace toolbar, select **Import notebook**, browse to your local repository's `src/notebooks` folder, and import `03_customer360_notebook_app.py`. Open the new notebook item.
3. Use **Python (PySpark)** in the Spark notebook experience. The app uses `pyspark.sql` and the `spark` session to query tables; it is not a Python-only notebook and does not require Polars.
4. Select **Add lakehouse**, attach `lh_customer360`, and pin it as the **default Lakehouse**. Restart an already-running session if you change its default Lakehouse.
5. Review the code and select **Run all**. This notebook reads existing tables and displays controls; it does not create or overwrite `customer_segments`.
6. Choose a **Segment** and/or **Customer** and select **Refresh** to update the overview, recent transactions, and voice-of-customer feedback. Select **All** to clear a filter. Both filters apply together.
7. Check that the displayed data matches your selection. Transaction and feedback details are limited to the first 25 customers in the filtered overview, ordered by lifetime value, with up to 100 rows displayed in each detail section.

---

## What we demonstrated in this workshop

1. **OneLake unification**: structured + unstructured data in one analytics plane.
2. **Shortcut strategy**: avoid duplicate storage, ingest through virtualized access.
3. **AI-ready feedback**: sentiment and redaction without building a custom model.
4. **Actionability**: retention risk and segment insights tied to real customers.
5. **Business readiness**: dashboard + app for analyst and account teams.

---
