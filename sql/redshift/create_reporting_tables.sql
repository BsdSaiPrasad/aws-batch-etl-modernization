CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.dim_customer (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    dw_created_at TIMESTAMP DEFAULT GETDATE()
);

CREATE TABLE IF NOT EXISTS analytics.dim_agent (
    agent_id INT PRIMARY KEY,
    agent_name VARCHAR(255),
    region VARCHAR(100),
    dw_created_at TIMESTAMP DEFAULT GETDATE()
);

CREATE TABLE IF NOT EXISTS analytics.dim_policy (
    policy_id INT PRIMARY KEY,
    customer_id INT,
    agent_id INT,
    policy_type VARCHAR(100),
    premium_amount DOUBLE PRECISION,
    policy_status VARCHAR(50),
    start_date DATE,
    end_date DATE,
    dw_created_at TIMESTAMP DEFAULT GETDATE()
);

CREATE TABLE IF NOT EXISTS analytics.fact_claim (
    claim_id INT PRIMARY KEY,
    policy_id INT,
    claim_status VARCHAR(50),
    claim_date DATE,
    claim_amount DOUBLE PRECISION,
    source_updated_ts TIMESTAMP,
    dw_created_at TIMESTAMP DEFAULT GETDATE()
);

CREATE TABLE IF NOT EXISTS analytics.fact_payment (
    payment_id INT PRIMARY KEY,
    policy_id INT,
    payment_method VARCHAR(50),
    payment_date DATE,
    payment_amount DOUBLE PRECISION,
    dw_created_at TIMESTAMP DEFAULT GETDATE()
);
