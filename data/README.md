# Data

This folder contains customer, order, support, and feedback datasets for the OneLake lab. The mix of CSV, Parquet, JSON, and plain-text files lets you explore structured and unstructured data together.

## Folder layout

- [raw/](./raw/) contains the source datasets.
- [curated/](./curated/) is currently empty; it provides a place for prepared datasets.

## Datasets

| Dataset | Format | Contents |
| --- | --- | --- |
| [Customers](./raw/customers.csv) | CSV | 250 customers, with their segment, location, and signup date. |
| [Orders](./raw/orders.parquet) | Parquet | Customer purchases, with order dates, products, and amounts. |
| [Support cases](./raw/support_cases.json) | JSON | An array of 206 support cases, with status, issue type, and priority. |
| [Customer feedback](./raw/feedback/) | Plain text | 250 files, one per customer, containing a short feedback statement. |

### Customers

Each row in `customers.csv` describes a customer:

- `customer`: Customer identifier, such as `CUST0001`.
- `segment`: Consumer, SMB, Mid-Market, or Enterprise.
- `location`: Customer city and country.
- `signup_date`: Signup date in `YYYY-MM-DD` format.

### Orders

The columns in `orders.parquet` are:

- `customer`: Customer identifier.
- `order_date`: Date of the order.
- `product`: Purchased product or offering.
- `amount`: Order amount.

The dataset does not include a currency column; do not assume a currency from the amount alone.

### Support cases

Each object in `support_cases.json` contains:

- `case_id`: Support case identifier, such as `CASE000001`.
- `customer`: Customer identifier.
- `opened_date`: Case opening date in `YYYY-MM-DD` format.
- `status`: Case status, such as Open, Closed, or Escalated.
- `issue_type`: Issue category, such as Billing, Performance, or Integration.
- `priority`: Case priority, such as Low, Medium, or High.

### Customer feedback

Files in [feedback/](./raw/feedback/) are named after the customer identifier, from `CUST0001.txt` through `CUST0250.txt`. Each statement includes the customer identifier, location, segment, and feedback about the product or service.

## How the datasets relate

Use the `customer` field to join customers with orders and support cases. For feedback, use the filename without the `.txt` extension as the customer identifier.

These relationships let you combine customer attributes, purchase activity, support history, and written feedback into a customer-level view. Aggregate orders and support cases by customer before joining when you want one row per customer, so multiple records do not multiply each other.
