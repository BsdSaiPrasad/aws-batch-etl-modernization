import json
import boto3

s3 = boto3.client("s3")

BUCKET_NAME = "batch-etl-modernization-dev-curated"
EXPECTED_DATASETS = [
    "std_customers",
    "std_agents",
    "std_policies",
    "std_claims",
    "std_payments"
]

def lambda_handler(event, context):
    load_date = event.get("load_date", "2026-03-29")
    missing = []

    for dataset in EXPECTED_DATASETS:
        prefix = f"dataset={dataset}/load_date={load_date}/"
        response = s3.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=prefix,
            MaxKeys=1
        )

        if "Contents" not in response:
            missing.append(dataset)

    if missing:
        return {
            "statusCode": 200,
            "status": "failure",
            "load_date": load_date,
            "missing_datasets": missing
        }

    return {
        "statusCode": 200,
        "status": "success",
        "load_date": load_date,
        "message": "All expected curated datasets are present"
    }
