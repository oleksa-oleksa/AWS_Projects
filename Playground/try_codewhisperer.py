# AWS
# create a function for S3 bucket
import boto3
import os
import json
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3_client = boto3.client("s3")
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client("s3", region_name=region)
            location = {"LocationConstraint": region}
            s3_client.create_bucket(
                Bucket=bucket_name, CreateBucketConfiguration=location
            )
    except ClientError as e:
        print(e)
        return False
    return True


# create a function to upload a file to S3 bucket
def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print(e)
        return False
    return True

# create a function to check the file size in S3 bucket
def get_file_size(bucket, object_name):
    s3_client = boto3.client("s3")
    try:
        response = s3_client.head_object(Bucket=bucket, Key=object_name)
    except ClientError as e:
        print(e)
        return False
    return response["ContentLength"]