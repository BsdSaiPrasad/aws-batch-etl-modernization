import os
import boto3

BUCKET_NAME = "batch-etl-modernization-dev-raw"
BASE_EXPORT_DIR = "data_exports"

s3 = boto3.client("s3")

for root, dirs, files in os.walk(BASE_EXPORT_DIR):
    for file in files:
        if file == ".DS_Store" or not file.endswith(".csv"):
            continue

        local_path = os.path.join(root, file)
        parts = local_path.split(os.sep)

        # expected: data_exports/load_date=YYYY-MM-DD/table/file.csv
        if len(parts) < 4:
            print(f"Skipping unexpected path: {local_path}")
            continue

        load_date = parts[1]
        table_name = parts[2]

        s3_key = f"source=postgres/table={table_name}/{load_date}/{file}"

        print(f"Uploading {local_path} -> s3://{BUCKET_NAME}/{s3_key}")
        s3.upload_file(local_path, BUCKET_NAME, s3_key)

print("Upload complete.")
