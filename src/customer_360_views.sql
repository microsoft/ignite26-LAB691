-- Run this in the Lakehouse SQL endpoint after creating the Delta tables.

CREATE OR ALTER VIEW [vw_customer_360] AS
SELECT
    [cs].[customer],
    [cs].[segment],
    [cs].[location],
    [cs].[signup_date],
    [cs].[lifetime_value],
    [cs].[order_count],
    [cs].[order_frequency_per_month],
    [cs].[days_since_last_purchase],
    [cs].[average_sentiment],
    [cs].[support_case_count],
    [cs].[retention_risk],
    [cs].[value_tier],
    [cs].[engagement_tier]
FROM [lh_customer360].[dbo].[customer_segments] AS [cs];

CREATE OR ALTER VIEW vw_sales_monthly AS
SELECT
    DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1) AS sales_month,
    customer,
    product,
    SUM(amount) AS revenue
FROM orders
GROUP BY
    DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1),
    customer,
    product;

CREATE OR ALTER VIEW vw_retention_summary AS
SELECT
    segment,
    retention_risk,
    COUNT(*) AS customer_count,
    SUM(lifetime_value) AS segment_ltv
FROM customer_segments
GROUP BY segment, retention_risk;
