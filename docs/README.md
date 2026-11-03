# Documentation and references

Use this reference index alongside the [attendee instructions](../instructions/README.md). It collects the documentation linked in the workshop, organized in the order you encounter the topics. Repeated links are listed only once.

## OneLake shortcuts and access (Step 2)

| Documentation | When to use it |
| --- | --- |
| [Create a same-tenant OneLake shortcut](https://learn.microsoft.com/en-us/fabric/onelake/shortcuts/create-onelake-shortcut) | Connect the destination Lakehouse to a source folder in another Fabric item. |
| [Delegated authentication for OneLake shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcut-security#delegated-authentication) | Understand the alternative to pass-through access when a configured connection identity reads the source data. |

## AI-powered shortcut transformations (Step 3)

| Documentation | When to use it |
| --- | --- |
| [Shortcut transformations (AI-powered)](https://learn.microsoft.com/en-us/fabric/onelake/shortcuts/transformations-ai) | Review prerequisites, supported text transformations, sentiment analysis, PII detection, synchronization, and preview limitations. |
| [Create a table shortcut with data transformation](https://learn.microsoft.com/en-us/fabric/onelake/shortcuts/transformations#create-a-table-shortcut-with-data-transformation) | Follow the destination table-shortcut workflow and review naming and subfolder settings. This page covers file transformations; use the AI-powered page for text processing. |
| [Azure Language regional support](https://learn.microsoft.com/en-us/azure/ai-services/language-service/concepts/regional-support) | Check the regional availability referenced by the AI-powered transformation documentation. |

## Fabric notebooks and runtime selection (Steps 4, 5, and 7)

| Documentation | When to use it |
| --- | --- |
| [Import existing notebooks into Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook#import-existing-notebooks) | Import local notebook source files, including `.py` files, as Fabric notebook items. |
| [Access the Python notebook experience](https://learn.microsoft.com/en-us/fabric/data-engineering/using-python-experience-on-notebook#how-to-access-a-python-notebook) | Learn how to select the pure Python experience for code without Spark dependencies. The lab notebooks use Spark and require Python (PySpark). |

## SQL analytics and Power BI semantic models (Step 6)

| Documentation | When to use it |
| --- | --- |
| [Create a Power BI semantic model in the Fabric portal](https://learn.microsoft.com/en-us/fabric/data-warehouse/create-semantic-model#create-a-new-power-bi-semantic-model-in-direct-lake-mode) | Create a semantic model from the SQL analytics endpoint, edit it in the browser, and create a report. |
| [Direct Lake overview and connection options](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview) | Understand Direct Lake on SQL versus Direct Lake on OneLake and why SQL views require DirectQuery fallback in the endpoint-based model. |

## Linked lab code

These repository files are also linked from the attendee instructions:

- [Polars segmentation notebook](../src/notebooks/02_polars_segmentation.py) - Builds the `customer_segments` Delta table in Step 5.
- [Customer 360 SQL views](../src/customer_360_views.sql) - Defines customer detail, monthly sales, and retention summary views in Step 6.
- [Customer 360 notebook app](../src/notebooks/03_customer360_notebook_app.py) - Provides interactive customer, transaction, and feedback exploration in Step 7.
