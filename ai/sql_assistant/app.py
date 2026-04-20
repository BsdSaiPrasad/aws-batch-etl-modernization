import os
import time
import boto3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Claims Analytics AI", layout="wide")

SCHEMA_CONTEXT = """
Available Redshift analytics tables:

analytics.dim_policy
- policy_id
- customer_id
- agent_id
- policy_type
- premium_amount
- policy_status
- start_date
- end_date

analytics.fact_claim
- claim_id
- policy_id
- claim_status
- claim_date
- claim_amount
- source_updated_ts

analytics.fact_payment
- payment_id
- policy_id
- payment_method
- payment_date
- payment_amount

Common join:
- analytics.fact_claim.policy_id = analytics.dim_policy.policy_id
- analytics.fact_payment.policy_id = analytics.dim_policy.policy_id
"""

BANNED_SQL = [
    "insert ", "update ", "delete ", "drop ", "alter ", "truncate ",
    "create ", "grant ", "revoke "
]

def generate_sql_fallback(question: str) -> str:
    q = question.lower().strip()

    if "rejected" in q and "policy" in q and ("amount" in q or "claim amount" in q):
        return """
SELECT
  dp.policy_type,
  SUM(fc.claim_amount) AS total_rejected_claim_amount
FROM analytics.fact_claim fc
JOIN analytics.dim_policy dp
  ON fc.policy_id = dp.policy_id
WHERE LOWER(fc.claim_status) = 'rejected'
GROUP BY dp.policy_type
ORDER BY total_rejected_claim_amount DESC
LIMIT 20
""".strip()

    if "claim count" in q and "status" in q:
        return """
SELECT
  claim_status,
  COUNT(*) AS claim_count
FROM analytics.fact_claim
GROUP BY claim_status
ORDER BY claim_count DESC
""".strip()

    if "payment" in q and "policy" in q:
        return """
SELECT
  dp.policy_type,
  SUM(fp.payment_amount) AS total_payment_amount
FROM analytics.fact_payment fp
JOIN analytics.dim_policy dp
  ON fp.policy_id = dp.policy_id
GROUP BY dp.policy_type
ORDER BY total_payment_amount DESC
LIMIT 20
""".strip()

    if "claim amount" in q and "policy" in q:
        return """
SELECT
  dp.policy_type,
  SUM(fc.claim_amount) AS total_claim_amount
FROM analytics.fact_claim fc
JOIN analytics.dim_policy dp
  ON fc.policy_id = dp.policy_id
GROUP BY dp.policy_type
ORDER BY total_claim_amount DESC
LIMIT 20
""".strip()

    return """
SELECT
  fc.claim_status,
  COUNT(*) AS claim_count,
  SUM(fc.claim_amount) AS total_claim_amount
FROM analytics.fact_claim fc
GROUP BY fc.claim_status
ORDER BY total_claim_amount DESC
LIMIT 20
""".strip()

def is_safe_select_sql(sql: str) -> tuple[bool, str]:
    cleaned = sql.strip().lower()

    if not cleaned:
        return False, "SQL is empty."

    if ";" in cleaned[:-1]:
        return False, "Only a single statement is allowed."

    if not (cleaned.startswith("select") or cleaned.startswith("with")):
        return False, "Only SELECT/CTE queries are allowed."

    for banned in BANNED_SQL:
        if banned in cleaned:
            return False, f"Blocked keyword found: {banned.strip()}"

    return True, "OK"

def run_redshift_query(sql: str) -> pd.DataFrame:
    workgroup = os.environ["WORKGROUP_NAME"]
    database = os.environ["DATABASE_NAME"]
    secret_arn = os.environ["SECRET_ARN"]

    client = boto3.client("redshift-data", region_name="us-east-1")

    resp = client.execute_statement(
        WorkgroupName=workgroup,
        Database=database,
        SecretArn=secret_arn,
        Sql=sql
    )
    statement_id = resp["Id"]

    start_time = time.time()

    while True:
        desc = client.describe_statement(Id=statement_id)
        status = desc["Status"]

        if status == "FINISHED":
            result = client.get_statement_result(Id=statement_id)
            break
        if status in ["FAILED", "ABORTED"]:
            raise RuntimeError(desc.get("Error", f"Query {status}"))
        if time.time() - start_time > 180:
            raise RuntimeError(f"Query timed out after 180 seconds. Last status: {status}")
        time.sleep(2)

    columns = [c["name"] for c in result["ColumnMetadata"]]
    rows = []

    for record in result["Records"]:
        row = []
        for field in record:
            if "stringValue" in field:
                row.append(field["stringValue"])
            elif "longValue" in field:
                row.append(field["longValue"])
            elif "doubleValue" in field:
                row.append(field["doubleValue"])
            elif "booleanValue" in field:
                row.append(field["booleanValue"])
            else:
                row.append(None)
        rows.append(row)

    return pd.DataFrame(rows, columns=columns)

st.title("Claims Analytics AI Assistant")
st.caption("Natural language to SQL over Redshift analytics tables")

with st.expander("Schema context", expanded=False):
    st.code(SCHEMA_CONTEXT)

question = st.text_input(
    "Ask a business question",
    placeholder="Which policy type has the highest rejected claim amount?"
)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Generate SQL", use_container_width=True) and question:
        st.session_state["generated_sql"] = generate_sql_fallback(question)

with col2:
    if st.button("Clear", use_container_width=True):
        st.session_state["generated_sql"] = ""

sql_value = st.text_area(
    "Generated SQL",
    value=st.session_state.get("generated_sql", ""),
    height=240
)

if st.button("Run SQL", use_container_width=True):
    ok, msg = is_safe_select_sql(sql_value)
    if not ok:
        st.error(msg)
    else:
        try:
            df = run_redshift_query(sql_value)
            st.success("Query executed successfully.")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(str(e))

st.markdown("### Example questions")
st.markdown("- Which policy type has the highest rejected claim amount?")
st.markdown("- Show claim count by status")
st.markdown("- Show total payments by policy type")
st.markdown("- Show total claim amount by policy type")
