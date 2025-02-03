import pandas as pd
import random
from datetime import datetime, timedelta

# Define clients
clients = ["client_001", "client_002", "client_003"]

# Bank-specific email categories and templates
bank_email_categories = {
    "Service Outage Notification": "We are currently experiencing an outage affecting online transactions.",
    "Security Incident Report": "We detected suspicious activity on our accounts. Please investigate.",
    "API Downtime Inquiry": "Can you provide an update on the recent API downtime?",
    "Regulatory Compliance Request": "We need confirmation that your service meets regulatory compliance.",
    "Service Upgrade Confirmation": "We have successfully upgraded to the new service tier.",
    "Billing Dispute": "There is a discrepancy in our latest invoice. Please review and clarify."
}

# Function to generate unique emails per client
def generate_unique_emails(client_id, start_email_id, start_date, num_emails=5):
    emails = []
    used_categories = set()
    for _ in range(num_emails):
        available_categories = list(set(bank_email_categories.keys()) - used_categories)
        if not available_categories:
            used_categories.clear()
            available_categories = list(bank_email_categories.keys())

        category = random.choice(available_categories)
        used_categories.add(category)
        
        timestamp = start_date + timedelta(days=random.randint(1, 30), hours=random.randint(8, 20))

        emails.append([
            client_id,
            f"email_{start_email_id}",
            timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            category,
            bank_email_categories[category]
        ])
        start_email_id += 1
    return emails, start_email_id

# Generate dataset
start_date = datetime(2024, 1, 1)
email_id_counter = 1
data = []

for client in clients:
    client_emails, email_id_counter = generate_unique_emails(client, email_id_counter, start_date, num_emails=7)
    data.extend(client_emails)

# Create DataFrame
df = pd.DataFrame(data, columns=["client_id", "email_id", "timestamp", "subject", "email_body"])

# Save as CSV
df.to_csv("synthetic_email_data.csv", index=False)
print("Dataset saved as synthetic_email_data.csv")
