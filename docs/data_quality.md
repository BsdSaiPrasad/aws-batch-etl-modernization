# Data Quality Plan

## Goal
Add simple but realistic data quality checks to the pipeline.

## Initial Checks
### Raw ingestion checks
- file exists in S3 raw
- expected number of source tables exported
- row count comparison between Postgres export and raw CSV

### Standardized/curated checks
- required columns not null
- duplicate business keys
- date parsing validity
- row count sanity check
- allowed status values

## Example Checks by Table

### customers
- customer_id not null
- customer_id unique
- email not null

### policies
- policy_id not null
- policy_id unique
- customer_id not null
- policy_status in allowed set

### claims
- claim_id not null
- claim_id unique
- policy_id not null
- claim_amount >= 0

### payments
- payment_id not null
- payment_id unique
- payment_amount >= 0

## Why This Matters
- teaches real DE practices
- makes pipeline more believable
- supports interview discussion around validation and failure handling