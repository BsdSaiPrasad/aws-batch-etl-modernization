CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.staging_customers (
    customer_id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    ingested_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.staging_agents (
    agent_id INT,
    agent_name VARCHAR(255),
    region VARCHAR(100),
    ingested_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.staging_policies (
    policy_id INT,
    customer_id INT,
    agent_id INT,
    policy_type VARCHAR(100),
    premium_amount DOUBLE PRECISION,
    policy_status VARCHAR(50),
    start_date DATE,
    end_date DATE,
    ingested_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.staging_claims (
    claim_id INT,
    policy_id INT,
    claim_amount DOUBLE PRECISION,
    claim_status VARCHAR(50),
    claim_date DATE,
    source_updated_ts TIMESTAMP,
    ingested_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.staging_payments (
    payment_id INT,
    policy_id INT,
    payment_amount DOUBLE PRECISION,
    payment_date DATE,
    payment_method VARCHAR(50),
    ingested_at TIMESTAMP
);
