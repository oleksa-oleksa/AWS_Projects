# Define the AWS provider
provider "aws" {
  region = "eu-west-1"
}

# Create an S3 bucket
resource "aws_s3_bucket" "customer-chunk-genai-project" {
  bucket = "customer_behaviour_data"

  tags = {
    Name        = "GenAI Project S3 Bucket"
    Environment = "Development"
  }
}

# Create folder structure using S3 objects
resource "aws_s3_object" "folders" {
  for_each = toset(["raw/", "processed/", "models/"])

  bucket = aws_s3_bucket.customer-chunk-genai-project.bucket
  key    = each.value
  content = "" # Empty content to simulate a folder
}

# Enable versioning for the bucket
resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.customer-chunk-genai-project.id

  versioning_configuration {
    status = "Enabled"
  }
}
