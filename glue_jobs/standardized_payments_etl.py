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

input_path = "s3://batch-etl-modernization-dev-raw/source=postgres/table=payments/"
output_path = f"s3://batch-etl-modernization-dev-curated/dataset=std_payments/load_date={load_date}/"

df = spark.read.option("header", "true").csv(input_path)

df_filtered = df.filter(F.col("load_date") == load_date)

df_standardized = (
    df_filtered
    .select(
        F.col("payment_id").cast("int").alias("payment_id"),
        F.col("policy_id").cast("int").alias("policy_id"),
        F.col("payment_amount").cast("double").alias("payment_amount"),
        F.to_date(F.col("payment_date")).alias("payment_date"),
        F.upper(F.trim(F.col("payment_method"))).alias("payment_method"),
        F.col("load_date")
    )
    .withColumn("ingested_at", F.current_timestamp())
)

df_standardized.write.mode("overwrite").parquet(output_path)

print(f"Payments standardized for load_date={load_date} and written to {output_path}")
