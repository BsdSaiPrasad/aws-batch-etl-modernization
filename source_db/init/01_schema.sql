CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE agents (
    agent_id INT PRIMARY KEY,
    agent_name VARCHAR(100),
    region VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE policies (
    policy_id INT PRIMARY KEY,
    customer_id INT,
    agent_id INT,
    policy_type VARCHAR(50),
    premium_amount NUMERIC(10,2),
    policy_status VARCHAR(20),
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
);

CREATE TABLE claims (
    claim_id INT PRIMARY KEY,
    policy_id INT,
    claim_amount NUMERIC(10,2),
    claim_status VARCHAR(20),
    claim_date DATE,
    source_updated_ts TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
);

CREATE TABLE payments (
    payment_id INT PRIMARY KEY,
    policy_id INT,
    payment_amount NUMERIC(10,2),
    payment_date DATE,
    payment_method VARCHAR(30),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
);
