import json
import boto3
import csv
import os
from urllib.parse import unquote_plus

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract bucket name and file name from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    # Skip files already processed (files in "headers/" folder or with "_header.csv" suffix)
    if file_key.startswith('headers/') or file_key.endswith('_header.csv'):
        print(f"Skipping already processed file: {file_key}")
        return {
            'statusCode': 200,
            'body': json.dumps('File already processed or in "headers/" folder')
        }
    
    # Get the CSV file from the S3 bucket
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        csv_content = response['Body'].read().decode('utf-8').splitlines()
        csv_reader = csv.reader(csv_content)
        header = next(csv_reader)  # Extract the header row
    except Exception as e:
        print(f"Error reading the file {file_key} from S3: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing the file')
        }

    # Create a new file name for the header CSV
    header_file_key = f"headers/{os.path.basename(file_key)}_header.csv"
    
    # Create CSV content with the header row
    header_content = '\n'.join([','.join(header)])

    # Upload the header CSV back to the S3 bucket in the "headers" folder
    try:
        s3.put_object(Bucket=bucket_name, Key=header_file_key, Body=header_content)
        print(f"Header extracted and saved as: {header_file_key}")
        return {
            'statusCode': 200,
            'body': json.dumps(f"Header extracted and saved as: {header_file_key}")
        }
    except Exception as e:
        print(f"Error saving header CSV: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error saving header file')
        }
