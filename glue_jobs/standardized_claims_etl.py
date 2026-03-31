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

input_path = "s3://batch-etl-modernization-dev-raw/source=postgres/table=claims/"
output_path = f"s3://batch-etl-modernization-dev-curated/dataset=std_claims/load_date={load_date}/"

df = spark.read.option("header", "true").csv(input_path)

df_filtered = df.filter(F.col("load_date") == load_date)

df_standardized = (
    df_filtered
    .select(
        F.col("claim_id").cast("int").alias("claim_id"),
        F.col("policy_id").cast("int").alias("policy_id"),
        F.col("claim_amount").cast("double").alias("claim_amount"),
        F.upper(F.trim(F.col("claim_status"))).alias("claim_status"),
        F.to_date(F.col("claim_date")).alias("claim_date"),
        F.to_timestamp(F.col("source_updated_ts")).alias("source_updated_ts"),
        F.col("load_date")
    )
    .withColumn("ingested_at", F.current_timestamp())
)

df_standardized.write.mode("overwrite").parquet(output_path)

print(f"Claims standardized for load_date={load_date} and written to {output_path}")
