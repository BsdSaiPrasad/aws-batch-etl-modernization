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

input_path = "s3://batch-etl-modernization-dev-raw/source=postgres/table=agents/"
output_path = f"s3://batch-etl-modernization-dev-curated/dataset=std_agents/load_date={load_date}/"

df = spark.read.option("header", "true").csv(input_path)

df_filtered = df.filter(F.col("load_date") == load_date)

df_standardized = (
    df_filtered
    .select(
        F.col("agent_id").cast("int").alias("agent_id"),
        F.trim(F.col("agent_name")).alias("agent_name"),
        F.trim(F.col("region")).alias("region"),
        F.col("load_date")
    )
    .withColumn("ingested_at", F.current_timestamp())
)

df_standardized.write.mode("overwrite").parquet(output_path)

print(f"Agents standardized for load_date={load_date} and written to {output_path}")
