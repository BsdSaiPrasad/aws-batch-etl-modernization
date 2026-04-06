import boto3

s3 = boto3.client("s3")

BUCKET_NAME = "batch-etl-modernization-dev-raw"
EXPECTED_TABLES = [
    "customers",
    "agents",
    "policies",
    "claims",
    "payments"
]

def lambda_handler(event, context):
    load_date = event.get("load_date", "2026-03-29")
    missing = []

    for table in EXPECTED_TABLES:
        prefix = f"source=postgres/table={table}/load_date={load_date}/"
        response = s3.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=prefix,
            MaxKeys=1
        )

        if "Contents" not in response:
            missing.append(table)

    if missing:
        return {
            "statusCode": 200,
            "status": "failure",
            "load_date": load_date,
            "missing_tables": missing
        }

    return {
        "statusCode": 200,
        "status": "success",
        "load_date": load_date,
        "message": "All expected raw source tables are present"
    }
