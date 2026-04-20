# AWS Batch ETL Modernization Platform

Modernizing a legacy insurance reporting workflow into a cloud-native batch analytics platform on AWS.

## Problem this project solves

Many organizations still depend on operational databases and manual CSV-based reporting workflows that are hard to scale, expensive to maintain, and slow for analytics. This project simulates that real-world problem and shows how to modernize it into a layered AWS data platform.

This platform solves for:

- moving data out of a legacy operational PostgreSQL system into a cloud data lake
- separating raw, standardized, and analytics-ready datasets
- transforming transactional data into dimensional and fact-style datasets for reporting
- validating and querying curated data with Athena and Redshift
- supporting dashboarding through QuickSight
- adding orchestration, monitoring, infrastructure-as-code, and CI/CD patterns
- exposing analytics through a natural-language-to-SQL assistant

In short: this project turns a fragile batch reporting setup into a more production-aligned AWS analytics platform.

---

## What this project includes

### Data pipeline
- Local PostgreSQL source system with insurance-style operational tables
- Python extraction and S3 ingestion
- AWS Glue standardized ETL layer
- Amazon EMR PySpark transformation layer
- Curated Parquet datasets in Amazon S3
- Athena validation on curated outputs
- Redshift analytics layer
- QuickSight dashboard over Redshift

### Platform and operations
- AWS IAM-based access setup
- SNS + CloudWatch alerting
- Terraform-managed monitoring resources
- GitHub Actions CI/CD workflow with branch + PR validation
- Branch-based Git workflow

### AI add-on
- Streamlit-based natural-language-to-SQL assistant
- Read-only SQL guardrails
- Redshift Data API execution
- Secrets Manager integration for credentials

---

## End-to-end architecture

```text
PostgreSQL / CSV sources
        |
        v
Python export + ingestion scripts
        |
        v
Amazon S3 Raw Zone
        |
        v
AWS Glue standardized ETL
        |
        v
Amazon S3 Standardized / Curated Zone
        |
        +--------------------> AWS Glue Data Catalog
        |                             |
        |                             v
        |                        Amazon Athena
        |
        v
Amazon EMR PySpark transformations
        |
        v
Curated analytics datasets in S3
        |
        v
Amazon Redshift analytics layer
        |
        +--------------------> Amazon QuickSight dashboards
        |
        +--------------------> Streamlit NL-to-SQL assistant
```
### Supporting services:
- AWS Step Functions
- AWS Lambda
- Amazon CloudWatch
- Amazon SNS
- AWS IAM
- Terraform
- GitHub Actions

## Project outcomes

This project demonstrates how to:

* ingest legacy operational data into an S3-based batch lake
* build standardized and analytics-ready datasets using PySpark
* use Athena to validate curated outputs
* expose reporting datasets in Redshift
* build QuickSight dashboards on top of the warehouse layer
* run heavier Spark workloads on EMR and write partitioned Parquet outputs
* provision monitoring resources with Terraform
* validate deployment workflows through GitHub Actions
* add a natural-language analytics interface on top of Redshift

⸻

### Tech stack

* Language: Python, SQL
* Source system: PostgreSQL
* Storage: Amazon S3
* ETL / processing: AWS Glue, Amazon EMR, PySpark
* Catalog / query: AWS Glue Data Catalog, Amazon Athena
* Warehouse: Amazon Redshift Serverless
* Dashboarding: Amazon QuickSight
* Orchestration: AWS Step Functions, AWS Lambda
* Monitoring: Amazon CloudWatch, Amazon SNS
* Infra as code: Terraform
* CI/CD: GitHub Actions
* AI interface: Streamlit + Redshift Data API + Secrets Manager

⸻

### Source data model

The local PostgreSQL source simulates an insurance domain with the following operational tables:

* customers
* agents
* policies
* claims
* payments

These are transformed into analytics-friendly outputs such as:

* dim_customer
* dim_agent
* dim_policy
* fact_claim
* fact_payment
* policy_claim_summary

⸻

## Lake and warehouse design

### Raw zone

Source extracts are landed into S3 in raw form.
s3://batch-etl-modernization-dev-raw/source=postgres/table=<table_name>/load_date=YYYY-MM-DD/<file>.csv

### Curated zone

Standardized and analytics-ready datasets are written back to S3 as partitioned Parquet.
s3://batch-etl-modernization-dev-curated/dataset=<dataset_name>/load_date=YYYY-MM-DD/

### Warehouse layer

Analytics datasets are exposed in Redshift for downstream BI and SQL access.

### Schemas used:

* staging
* analytics

Example analytics tables:

* analytics.dim_policy
* analytics.fact_claim
* analytics.fact_payment

⸻

## Key implemented components

1. Legacy source simulation

A local PostgreSQL system was created with seeded insurance-style operational data to simulate a real batch source.

2. Python-based source extraction and ingestion

Python scripts export source tables to CSV and upload them to Amazon S3 using partitioned load-date paths.

3. Glue standardized ETL layer

Glue jobs standardize source datasets into analytics-friendly intermediate outputs.

4. EMR heavy transformation layer

A PySpark job (policy_claim_summary.py) was executed successfully on Amazon EMR and wrote partitioned Parquet output to S3.

Verified output example:
s3://batch-etl-modernization-dev-curated/dataset=policy_claim_summary/load_date=2026-03-29/

5. Athena validation

Curated Parquet outputs were registered and queried through Athena to validate EMR-generated output and schema alignment.

6. Redshift analytics layer

Curated datasets were queried from Redshift and used as the serving layer for analytics and BI.

7. QuickSight dashboarding

QuickSight was connected to Redshift through a VPC connection. A custom SQL dataset was created and used to build visuals such as:

* total claim amount by policy type
* claim count by policy type and claim status
* overall claim status distribution

8. Terraform-managed monitoring resources

Terraform was used to provision a separate test environment for:

* SNS topic
* email subscription
* CloudWatch alarm for Step Functions failures

9. GitHub Actions CI/CD

A PR-based GitHub Actions workflow validates changes before merge, with dev and prod deployment stages separated in the workflow design.

10. AI analytics add-on

A Streamlit application was built to accept business questions in natural language, convert them to SQL, apply read-only safety checks, execute queries via Redshift Data API, and return results.

Example question:

Show claim count by status

Returned result:

* REJECTED: 510
* CLOSED: 504
* OPEN: 486

⸻

### Why these design choices

Why S3?

S3 provides a low-cost, durable raw and curated storage layer for batch ingestion and analytics datasets.

Why Glue and EMR together?

Glue is useful for standardized ETL patterns and managed Spark jobs. EMR is useful for heavier or more customized Spark workloads. This project intentionally shows both service choices and where each fits.

Why Athena?

Athena is a fast validation layer on top of curated S3 datasets without needing to load everything into a warehouse first.

Why Redshift?

Redshift provides a serving layer for analytics, BI, and dashboarding workloads where curated data can be queried efficiently.

Why QuickSight?

QuickSight demonstrates the downstream business consumption layer on top of the warehouse.

Why Terraform?

Terraform makes monitoring resources reproducible and version-controlled instead of manually configured.

Why an AI add-on?

The natural-language-to-SQL assistant shows how a modern analytics platform can expose warehouse data through a lightweight business-facing interface.

⸻

## Repository structure
```text 
aws-batch-etl-modernization/
├── README.md
├── .gitignore
├── docker-compose.yml
├── ai/
│   └── sql_assistant/
│       └── app.py
├── docs/
├── emr_jobs/
├── glue_jobs/
├── ingestion/
├── lambda/
├── source_db/
├── sql/
├── step_functions/
├── terraform/
└── tests/
```
## Quick start

1. Start the local source system

Use Docker Compose to bring up the PostgreSQL source.
docker-compose up -d

2. Extract source data locally

Run the export script to generate load-date partitioned extracts.
python source_db/scripts/export_to_csv.py

3. Upload raw data to S3

Push extracted files into the raw S3 zone.
python ingestion/upload_to_s3.py

4. Run standardized ETL

Run Glue-based standardization jobs for raw source datasets.

5. Run heavier Spark transformation on EMR

Submit the EMR Spark application for policy-level summary generation.

6. Validate output in Athena

Create or update Athena table definitions and query curated outputs.

7. Query analytics in Redshift

Load or expose analytics datasets in Redshift and validate business-facing queries.

8. Build BI views in QuickSight

Connect QuickSight to Redshift and create visuals.

9. Run the AI assistant

Start the Streamlit app and ask business questions against analytics tables.
python3 -m streamlit run ai/sql_assistant/app.py

## Example analytics questions supported

### SQL / BI layer

* Which policy type has the highest total claim amount?
* How many claims are in each status?
* What is the total payment amount by policy type?

### AI assistant

* Show claim count by status
* Show total payments by policy type
* Which policy type has the highest rejected claim amount?

## Production hardening ideas

If this were extended further toward production, the next improvements would be:

* formal data quality checks on standardized and curated datasets
* stronger schema enforcement and contract validation
* orchestration of the full end-to-end pipeline in Step Functions
* automated Redshift loads or dbt-based modeling
* better CI/CD deployment promotion across environments
* more robust AI-to-SQL generation using a real LLM
* SQL parser-based validation and query limits
* audit logging and usage tracking for the AI assistant
* secrets and config management through environment-specific deployment patterns

## Future enhancements

* dbt models for warehouse transformations
* full Step Functions orchestration of batch jobs
* Lambda-based pre-check and post-check validation
* automatic dataset refresh flows
* dashboard polishing and business KPI views
* LLM-powered SQL generation beyond rule-based fallback logic

⸻

## Author

### Sai Prasad
### Data Engineering / Analytics Engineering portfolio project built to simulate a production-style AWS batch modernization platform.
