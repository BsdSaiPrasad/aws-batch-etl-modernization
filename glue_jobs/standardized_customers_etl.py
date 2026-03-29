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

input_path = "s3://batch-etl-modernization-dev-raw/source=postgres/table=customers/"
output_path = f"s3://batch-etl-modernization-dev-curated/dataset=std_customers/load_date={load_date}/"

df = spark.read.option("header", "true").csv(input_path)

df_filtered = df.filter(F.col("load_date") == load_date)

df_standardized = (
    df_filtered
    .select(
        F.col("customer_id").cast("int").alias("customer_id"),
        F.trim(F.col("first_name")).alias("first_name"),
        F.trim(F.col("last_name")).alias("last_name"),
        F.lower(F.trim(F.col("email"))).alias("email"),
        F.trim(F.col("city")).alias("city"),
        F.trim(F.col("state")).alias("state"),
        F.col("load_date")
    )
    .withColumn("ingested_at", F.current_timestamp())
)

df_standardized.write.mode("overwrite").parquet(output_path)

print(f"Customers standardized for load_date={load_date} and written to {output_path}")
