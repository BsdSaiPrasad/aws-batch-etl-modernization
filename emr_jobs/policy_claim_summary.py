from pyspark.sql import SparkSession
from pyspark.sql import functions as F

LOAD_DATE = "2026-03-29"

spark = SparkSession.builder.appName("policy-claim-summary").getOrCreate()

base_path = "s3://batch-etl-modernization-dev-curated"

customers_path = f"{base_path}/dataset=std_customers/load_date={LOAD_DATE}/"
agents_path = f"{base_path}/dataset=std_agents/load_date={LOAD_DATE}/"
policies_path = f"{base_path}/dataset=std_policies/load_date={LOAD_DATE}/"
claims_path = f"{base_path}/dataset=std_claims/load_date={LOAD_DATE}/"
payments_path = f"{base_path}/dataset=std_payments/load_date={LOAD_DATE}/"

output_path = f"{base_path}/dataset=policy_claim_summary/load_date={LOAD_DATE}/"

customers_df = spark.read.parquet(customers_path)
agents_df = spark.read.parquet(agents_path)
policies_df = spark.read.parquet(policies_path)
claims_df = spark.read.parquet(claims_path)
payments_df = spark.read.parquet(payments_path)

claims_agg_df = (
    claims_df
    .groupBy("policy_id")
    .agg(
        F.count("*").alias("total_claim_count"),
        F.sum("claim_amount").alias("total_claim_amount"),
        F.max("claim_date").alias("last_claim_date")
    )
)

payments_agg_df = (
    payments_df
    .groupBy("policy_id")
    .agg(
        F.sum("payment_amount").alias("total_payment_amount")
    )
)

summary_df = (
    policies_df.alias("p")
    .join(customers_df.alias("c"), F.col("p.customer_id") == F.col("c.customer_id"), "left")
    .join(agents_df.alias("a"), F.col("p.agent_id") == F.col("a.agent_id"), "left")
    .join(claims_agg_df.alias("cl"), F.col("p.policy_id") == F.col("cl.policy_id"), "left")
    .join(payments_agg_df.alias("pm"), F.col("p.policy_id") == F.col("pm.policy_id"), "left")
    .select(
        F.col("p.policy_id").alias("policy_id"),
        F.col("p.customer_id").alias("customer_id"),
        F.col("p.agent_id").alias("agent_id"),
        F.concat_ws(" ", F.col("c.first_name"), F.col("c.last_name")).alias("customer_name"),
        F.col("a.agent_name").alias("agent_name"),
        F.col("p.policy_type").alias("policy_type"),
        F.col("p.policy_status").alias("policy_status"),
        F.col("p.premium_amount").alias("premium_amount"),
        F.coalesce(F.col("cl.total_claim_count"), F.lit(0)).alias("total_claim_count"),
        F.coalesce(F.col("cl.total_claim_amount"), F.lit(0.0)).alias("total_claim_amount"),
        F.coalesce(F.col("pm.total_payment_amount"), F.lit(0.0)).alias("total_payment_amount"),
        F.col("cl.last_claim_date").alias("last_claim_date")
    )
    .withColumn("ingested_at", F.current_timestamp())
)

summary_df.write.mode("overwrite").parquet(output_path)

print(f"policy_claim_summary written to {output_path}")

spark.stop()
