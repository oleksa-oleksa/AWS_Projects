from google.cloud import bigquery

# Initialize BigQuery client
client = bigquery.Client()

# Define dataset and table
dataset_id = "your_project_id.customer_sentiment"
table_id = f"{dataset_id}.email_sentiment"

# Load CSV file into BigQuery
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True,  # Auto-detect schema
)

with open("synthetic_email_data.csv", "rb") as source_file:
    job = client.load_table_from_file(source_file, table_id, job_config=job_config)

job.result()  # Wait for job to complete
print(f"Uploaded {job.output_rows} rows to {table_id}.")
