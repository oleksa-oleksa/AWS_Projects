from openai import OpenAI
import os
import pandas as pd
from google.cloud import bigquery

# Load BigQuery Data
bigquery_client = bigquery.Client()

query = "SELECT client_id, email_id, email_body FROM `mmbtestproject.customer_sentiment.email_sentiment`"
df = bigquery_client.query(query).to_dataframe()

# OpenAI API Key (Replace with your key)
openai_key = os.environ.get("OPENAI_API_KEY")
ai_client = OpenAI(
    api_key=openai_key,  # This is the default and can be omitted
)

# Function to analyze sentiment
def analyze_sentiment(email_body):

    completion = ai_client.chat.completions.create(
      model="gpt-4o-mini",
      store=True,
      messages=[{"role": "user", "content": f"Analyze sentiment: {email_body}"}]
    )
    
    return completion.choices[0].message.content
  
# Apply sentiment analysis
df["sentiment"] = df["email_body"].apply(analyze_sentiment)

# Print sample results
print(df.head())
