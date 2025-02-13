import json
import pandas as pd
from google.cloud import bigquery, aiplatform

def extract_features_from_bigquery(project_id, dataset_id, table_id):
    client = bigquery.Client(project=project_id)
    query = f"""
        SELECT * FROM `{project_id}.{dataset_id}.{table_id}`
    """
    df = client.query(query).to_dataframe()
    return df

def analyze_with_gemini(client_data):
    aiplatform.init(project="your-gcp-project")
    model = aiplatform.generation.TextGenerationModel.from_pretrained("gemini-pro")
    
    prompt = (
        "Analyze the risk of client churn based on the following data: "
        + json.dumps(client_data, indent=2)
    )
    
    response = model.predict(prompt)
    return response.text

def store_results_in_bigquery(project_id, dataset_id, table_id, results):
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    errors = client.insert_rows_json(table_ref, results)
    if errors:
        print("BigQuery insertion errors:", errors)
    else:
        print("Results successfully stored in BigQuery.")

def main():
    project_id = "your-gcp-project"
    dataset_id = "your_dataset"
    source_table_id = "client_features"
    result_table_id = "churn_predictions"
    
    # Extract client features
    client_data = extract_features_from_bigquery(project_id, dataset_id, source_table_id)
    
    results = []
    for _, row in client_data.iterrows():
        response_text = analyze_with_gemini(row.to_dict())
        results.append({"Client_ID": row["Client_ID"], "Churn_Analysis": response_text})
    
    # Store results in BigQuery
    store_results_in_bigquery(project_id, dataset_id, result_table_id, results)
    
if __name__ == "__main__":
    main()
