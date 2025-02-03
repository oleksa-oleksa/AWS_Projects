import pandas as pd
import random
from datetime import datetime, timedelta

# Generate synthetic email data for 3 clients (4-7 emails per client)
clients = ["client_001", "client_002", "client_003"]
categories = ["Signed Contract", "Reported Issue", "Asking for Help", "General Inquiry"]
subjects = {
    "Signed Contract": "Contract Signed - Welcome to Our Service",
    "Reported Issue": "Urgent: Issue with Banking Transactions",
    "Asking for Help": "Need Assistance with Account Access",
    "General Inquiry": "Question about Service Fees"
}
email_templates = {
    "Signed Contract": "Dear Team, we are pleased to confirm that we have signed the contract.",
    "Reported Issue": "We are experiencing issues with our banking transactions. Please resolve ASAP.",
    "Asking for Help": "Can you help us regain access to our account? We are unable to log in.",
    "General Inquiry": "Can you provide details about the latest service fees?"
}

data = []
email_id_counter = 1
start_date = datetime(2024, 1, 1)

for client in clients:
    num_emails = random.randint(4, 7)
    for _ in range(num_emails):
        category = random.choice(categories)
        timestamp = start_date + timedelta(days=random.randint(1, 30), hours=random.randint(8, 20))
        sentiment_score = round(random.uniform(-1, 1), 2)  # -1 (negative) to 1 (positive)

        data.append([
            client,
            f"email_{email_id_counter}",
            timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            subjects[category],
            email_templates[category],
            category,
            sentiment_score
        ])
        email_id_counter += 1

# Create DataFrame
df = pd.DataFrame(data, columns=["client_id", "email_id", "timestamp", "subject", "email_body", "category", "sentiment_score"])

# Save as CSV
csv_filename = "/mnt/data/synthetic_email_data.csv"
df.to_csv(csv_filename, index=False)
csv_filename
