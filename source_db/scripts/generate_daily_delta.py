import random
import psycopg2
from datetime import datetime, timedelta

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="legacy_insurance",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

now = datetime.now()

# -------------------------
# Customers
# -------------------------
existing_customer_ids = set()
cur.execute("SELECT customer_id FROM customers")
for row in cur.fetchall():
    existing_customer_ids.add(row[0])

for customer_id in range(6, 101):
    if customer_id in existing_customer_ids:
        continue
    first_name = f"Customer{customer_id}"
    last_name = "User"
    email = f"customer{customer_id}@email.com"
    city = random.choice(["Dallas", "Austin", "Seattle", "Chicago", "San Jose", "New York", "Phoenix"])
    state = random.choice(["TX", "WA", "IL", "CA", "NY", "AZ"])
    cur.execute("""
        INSERT INTO customers (customer_id, first_name, last_name, email, city, state, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
    """, (customer_id, first_name, last_name, email, city, state))

# -------------------------
# Agents
# -------------------------
existing_agent_ids = set()
cur.execute("SELECT agent_id FROM agents")
for row in cur.fetchall():
    existing_agent_ids.add(row[0])

for agent_id in range(104, 111):
    if agent_id in existing_agent_ids:
        continue
    agent_name = f"Agent{agent_id}"
    region = random.choice(["South", "West", "Midwest", "Northeast"])
    cur.execute("""
        INSERT INTO agents (agent_id, agent_name, region, created_at, updated_at)
        VALUES (%s, %s, %s, NOW(), NOW())
    """, (agent_id, agent_name, region))

# -------------------------
# Policies
# -------------------------
existing_policy_ids = set()
cur.execute("SELECT policy_id FROM policies")
for row in cur.fetchall():
    existing_policy_ids.add(row[0])

for policy_id in range(1006, 1501):
    if policy_id in existing_policy_ids:
        continue
    customer_id = random.randint(1, 100)
    agent_id = random.randint(101, 110)
    policy_type = random.choice(["Auto", "Health", "Life", "Home"])
    premium_amount = round(random.uniform(500, 5000), 2)
    policy_status = random.choice(["ACTIVE", "LAPSED", "CANCELLED"])
    start_date = now.date() - timedelta(days=random.randint(1, 900))
    end_date = start_date + timedelta(days=365)
    cur.execute("""
        INSERT INTO policies (
            policy_id, customer_id, agent_id, policy_type, premium_amount,
            policy_status, start_date, end_date, created_at, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
    """, (policy_id, customer_id, agent_id, policy_type, premium_amount, policy_status, start_date, end_date))

# -------------------------
# Claims
# -------------------------
existing_claim_ids = set()
cur.execute("SELECT claim_id FROM claims")
for row in cur.fetchall():
    existing_claim_ids.add(row[0])

for claim_id in range(5005, 6501):
    if claim_id in existing_claim_ids:
        continue
    policy_id = random.randint(1001, 1500)
    claim_amount = round(random.uniform(100, 10000), 2)
    claim_status = random.choice(["OPEN", "CLOSED", "REJECTED"])
    claim_date = now.date() - timedelta(days=random.randint(1, 365))
    source_updated_ts = now - timedelta(days=random.randint(0, 30))
    cur.execute("""
        INSERT INTO claims (
            claim_id, policy_id, claim_amount, claim_status, claim_date,
            source_updated_ts, created_at, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
    """, (claim_id, policy_id, claim_amount, claim_status, claim_date, source_updated_ts))

# -------------------------
# Payments
# -------------------------
existing_payment_ids = set()
cur.execute("SELECT payment_id FROM payments")
for row in cur.fetchall():
    existing_payment_ids.add(row[0])

for payment_id in range(7006, 9501):
    if payment_id in existing_payment_ids:
        continue
    policy_id = random.randint(1001, 1500)
    payment_amount = round(random.uniform(50, 1000), 2)
    payment_date = now.date() - timedelta(days=random.randint(1, 365))
    payment_method = random.choice(["CARD", "BANK_TRANSFER", "UPI", "ACH"])
    cur.execute("""
        INSERT INTO payments (
            payment_id, policy_id, payment_amount, payment_date,
            payment_method, created_at, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
    """, (payment_id, policy_id, payment_amount, payment_date, payment_method))

conn.commit()
cur.close()
conn.close()

print("Synthetic data generation complete.")
