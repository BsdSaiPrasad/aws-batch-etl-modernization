
```md
# Runbook

## Purpose
This runbook documents how to start the project, run ingestion, and handle common issues.

---

## 1. Start PostgreSQL Source

From project root:

```bash
docker compose up -d
docker ps

Expected container:
	•	aws-batch-etl-postgres

2. Verify PostgreSQL Data

Open psql: 
    docker exec -it aws-batch-etl-postgres psql -U postgres -d legacy_insurance

Check tables:
    \dt
    SELECT * FROM customers;
    SELECT * FROM policies;
    SELECT * FROM claims;
    \q

3. Export Source Data to CSV
Run:
    python3 source_db/scripts/export_to_csv.py

Expected output:
	•	CSV files written under data_exports/load_date=YYYY-MM-DD/...

Verify:
    find data_exports -type f

4. Upload Raw Files to S3

Run:
    python3 ingestion/upload_to_s3.py

Expected S3 object structure:
    source=postgres/table=customers/load_date=YYYY-MM-DD/customers.csv
    source=postgres/table=claims/load_date=YYYY-MM-DD/claims.csv

Verify in AWS Console:
	•	bucket: batch-etl-modernization-dev-raw

5. Common Issues

Issue: pip: command not found

Use:
python3 -m pip install pandas psycopg2-binary boto3

Issue: AWS CLI not installed

Install:
brew install awscli

Verify:
aws --version

Issue: AWS credentials not configured

Run:
aws configure
aws sts get-caller-identity

Issue: .DS_Store causes ingestion failure

Mac hidden files may appear in exported folders. Upload logic should skip:
	•	.DS_Store
	•	non-CSV files
	•	unexpected path structures

Issue: S3 upload permission failure

Check:
	•	IAM user policies
	•	AWS CLI configured with correct account
	•	bucket name is correct
	•	region is us-east-1

Issue: PostgreSQL container not running

Run:
    docker compose up -d
    docker ps
Issue: Need to reset database initialization

If you need a full reset:
docker compose down -v
docker compose up -d
Warning: this removes local Postgres volume data.

6. Current AWS Resources
	•	S3 raw bucket: batch-etl-modernization-dev-raw
	•	S3 curated bucket: batch-etl-modernization-dev-curated
	•	SNS topic: batch-etl-modernization-dev-alerts
	•	IAM CLI user: batch-etl-dev-cli-user

7. Immediate Next Steps
	•	verify raw files landed in S3
	•	commit project to git
	•	add data quality checks
	•	build Glue standardized ETL layer