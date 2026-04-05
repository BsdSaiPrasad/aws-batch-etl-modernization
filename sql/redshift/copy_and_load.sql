-- COPY from curated S3 into staging
COPY staging.staging_customers
FROM 's3://batch-etl-modernization-dev-curated/dataset=std_customers/'
IAM_ROLE 'arn:aws:iam::720800607159:role/service-role/AmazonRedshift-CommandsAccessRole-20260404T182815'
FORMAT AS PARQUET;

COPY staging.staging_agents
FROM 's3://batch-etl-modernization-dev-curated/dataset=std_agents/'
IAM_ROLE 'arn:aws:iam::720800607159:role/service-role/AmazonRedshift-CommandsAccessRole-20260404T182815'
FORMAT AS PARQUET;

COPY staging.staging_policies
FROM 's3://batch-etl-modernization-dev-curated/dataset=std_policies/'
IAM_ROLE 'arn:aws:iam::720800607159:role/service-role/AmazonRedshift-CommandsAccessRole-20260404T182815'
FORMAT AS PARQUET;

COPY staging.staging_claims
FROM 's3://batch-etl-modernization-dev-curated/dataset=std_claims/'
IAM_ROLE 'arn:aws:iam::720800607159:role/service-role/AmazonRedshift-CommandsAccessRole-20260404T182815'
FORMAT AS PARQUET;

COPY staging.staging_payments
FROM 's3://batch-etl-modernization-dev-curated/dataset=std_payments/'
IAM_ROLE 'arn:aws:iam::720800607159:role/service-role/AmazonRedshift-CommandsAccessRole-20260404T182815'
FORMAT AS PARQUET;

-- Load analytics tables from staging
INSERT INTO analytics.dim_customer
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    city,
    state,
    GETDATE()
FROM staging.staging_customers;

INSERT INTO analytics.dim_agent
SELECT
    agent_id,
    agent_name,
    region,
    GETDATE()
FROM staging.staging_agents;

INSERT INTO analytics.dim_policy
SELECT
    policy_id,
    customer_id,
    agent_id,
    policy_type,
    premium_amount,
    policy_status,
    start_date,
    end_date,
    GETDATE()
FROM staging.staging_policies;

INSERT INTO analytics.fact_claim
SELECT
    claim_id,
    policy_id,
    claim_status,
    claim_date,
    claim_amount,
    source_updated_ts,
    GETDATE()
FROM staging.staging_claims;

INSERT INTO analytics.fact_payment
SELECT
    payment_id,
    policy_id,
    payment_method,
    payment_date,
    payment_amount,
    GETDATE()
FROM staging.staging_payments;

-- Validation checks
SELECT COUNT(*) AS dim_customer_count FROM analytics.dim_customer;
SELECT COUNT(*) AS dim_agent_count FROM analytics.dim_agent;
SELECT COUNT(*) AS dim_policy_count FROM analytics.dim_policy;
SELECT COUNT(*) AS fact_claim_count FROM analytics.fact_claim;
SELECT COUNT(*) AS fact_payment_count FROM analytics.fact_payment;
