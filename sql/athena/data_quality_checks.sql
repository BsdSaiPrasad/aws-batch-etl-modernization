-- Row counts for latest batch
SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM curated_dataset_std_customers
WHERE load_date = '2026-03-29'

UNION ALL

SELECT 'agents' AS table_name, COUNT(*) AS row_count
FROM curated_dataset_std_agents
WHERE load_date = '2026-03-29'

UNION ALL

SELECT 'policies' AS table_name, COUNT(*) AS row_count
FROM curated_dataset_std_policies
WHERE load_date = '2026-03-29'

UNION ALL

SELECT 'claims' AS table_name, COUNT(*) AS row_count
FROM curated_dataset_std_claims
WHERE load_date = '2026-03-29'

UNION ALL

SELECT 'payments' AS table_name, COUNT(*) AS row_count
FROM curated_dataset_std_payments
WHERE load_date = '2026-03-29';

-- Null checks
SELECT COUNT(*) AS null_customer_ids
FROM curated_dataset_std_customers
WHERE customer_id IS NULL
  AND load_date = '2026-03-29';

SELECT COUNT(*) AS null_policy_ids
FROM curated_dataset_std_policies
WHERE policy_id IS NULL
  AND load_date = '2026-03-29';

SELECT COUNT(*) AS null_claim_ids
FROM curated_dataset_std_claims
WHERE claim_id IS NULL
  AND load_date = '2026-03-29';

SELECT COUNT(*) AS null_payment_ids
FROM curated_dataset_std_payments
WHERE payment_id IS NULL
  AND load_date = '2026-03-29';

-- Duplicate key checks
SELECT customer_id, COUNT(*) AS cnt
FROM curated_dataset_std_customers
WHERE load_date = '2026-03-29'
GROUP BY customer_id
HAVING COUNT(*) > 1;

SELECT policy_id, COUNT(*) AS cnt
FROM curated_dataset_std_policies
WHERE load_date = '2026-03-29'
GROUP BY policy_id
HAVING COUNT(*) > 1;

SELECT claim_id, COUNT(*) AS cnt
FROM curated_dataset_std_claims
WHERE load_date = '2026-03-29'
GROUP BY claim_id
HAVING COUNT(*) > 1;

SELECT payment_id, COUNT(*) AS cnt
FROM curated_dataset_std_payments
WHERE load_date = '2026-03-29'
GROUP BY payment_id
HAVING COUNT(*) > 1;
