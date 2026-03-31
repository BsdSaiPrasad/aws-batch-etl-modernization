import sys
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'LOAD_DATE'])
load_date = args['LOAD_DATE']

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

input_path = "s3://batch-etl-modernization-dev-raw/source=postgres/table=policies/"
output_path = f"s3://batch-etl-modernization-dev-curated/dataset=std_policies/load_date={load_date}/"

df = spark.read.option("header", "true").csv(input_path)

df_filtered = df.filter(F.col("load_date") == load_date)

df_standardized = (
    df_filtered
    .select(
        F.col("policy_id").cast("int").alias("policy_id"),
        F.col("customer_id").cast("int").alias("customer_id"),
        F.col("agent_id").cast("int").alias("agent_id"),
        F.trim(F.col("policy_type")).alias("policy_type"),
        F.col("premium_amount").cast("double").alias("premium_amount"),
        F.upper(F.trim(F.col("policy_status"))).alias("policy_status"),
        F.to_date(F.col("start_date")).alias("start_date"),
        F.to_date(F.col("end_date")).alias("end_date"),
        F.col("load_date")
    )
    .withColumn("ingested_at", F.current_timestamp())
)

df_standardized.write.mode("overwrite").parquet(output_path)

print(f"Policies standardized for load_date={load_date} and written to {output_path}")
