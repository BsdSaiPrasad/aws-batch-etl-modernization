# AWS Batch ETL Modernization Platform

## Project Overview
This project simulates a real-world batch data engineering pipeline that modernizes a legacy operational reporting workflow using AWS services and local source systems.

The pipeline starts from a legacy-style PostgreSQL operational database and optional CSV extracts, lands raw data into Amazon S3, transforms it through AWS-style ETL stages, writes curated datasets back to S3, supports querying and validation, and later loads reporting-ready data into a warehouse layer.

## Architecture
Source systems:
- Legacy Operational Database (PostgreSQL)
- Flat Files / CSV Extracts
- Optional external source feed

Target AWS architecture:
- Amazon S3 Raw Zone
- AWS Glue standardized ETL layer
- Amazon EMR (Spark / PySpark) heavy transformation layer
- Amazon S3 Curated Zone
- AWS Glue Data Catalog
- Amazon Athena
- Amazon Redshift
- AWS Step Functions
- AWS Lambda
- Amazon CloudWatch
- Amazon SNS
- AWS IAM
- Terraform
- GitHub Actions CI/CD

## Current Status
Completed:
- AWS account setup
- Budget / cost guardrails
- Region selection: us-east-1
- Local project scaffold
- Local Git repo initialized
- Local PostgreSQL source system created with sample insurance-style tables
- Seed data loaded into PostgreSQL
- S3 buckets created
- SNS topic created with email subscription
- AWS CLI configured with IAM user
- Local export script created for extracting source tables to CSV
- Local upload script created for pushing raw files to S3
- Hidden-file ingestion issue identified (.DS_Store) and handled

In progress:
- Raw ingestion verification in S3
- Documentation
- First Git commit

Upcoming:
- AWS Glue standardized ETL layer
- Amazon EMR PySpark transformation layer
- Glue Data Catalog + Athena validation
- Redshift load
- Step Functions + Lambda orchestration
- CloudWatch + SNS monitoring flow
- Terraform + GitHub Actions CI/CD

## Source Schema
Local PostgreSQL source tables:
- customers
- agents
- policies
- claims
- payments

Planned curated outputs:
- dim_customer
- dim_agent
- dim_policy
- fact_claim
- fact_payment
- policy_claim_summary

## Local Project Structure
```text
aws-batch-etl-modernization/
├── README.md
├── .gitignore
├── docker-compose.yml
├── source_db/
├── ingestion/
├── glue_jobs/
├── emr_jobs/
├── sql/
├── lambda/
├── step_functions/
├── terraform/
├── tests/
└── docs/

S3 Layout

Raw
s3://batch-etl-modernization-dev-raw/source=postgres/table=<table_name>/load_date=YYYY-MM-DD/<file>.csv

Curated
s3://batch-etl-modernization-dev-curated/dataset=<dataset_name>/load_date=YYYY-MM-DD/

Why This Project

This project is designed to teach and demonstrate:
	•	source-to-lake batch ingestion
	•	raw zone design
	•	PySpark data transformation
	•	Glue vs EMR service choices
	•	data cataloging and validation
	•	warehouse loading patterns
	•	orchestration and monitoring
	•	IAM and cloud access fundamentals
	•	Terraform and CI/CD basics
	•	interview-ready explanation of real DE workflows

Tools Used So Far
	•	PostgreSQL (local Docker)
	•	Python
	•	pandas
	•	psycopg2
	•	boto3
	•	AWS S3
	•	AWS SNS
	•	AWS IAM
	•	AWS CLI
	•	Git

Next Steps
	1.	Verify S3 raw ingestion
	2.	Add data quality checks
	3.	Build Glue standardized ETL script
	4.	Build EMR PySpark transformation script
	5.	Add Athena + Glue Catalog
	6.	Add Redshift load
	7.	Add orchestration
	8.	Add Terraform + GitHub Actions
## CI/CD note
Using branch + PR flow for validation before merge.
