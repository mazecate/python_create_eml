import json
import os

# Updated sample JSON data with multiple companies
data = {
    "CompanyA": [
        {"username": "Peter Chan", "goh": "Mr. John Lam", "to": ["recipient1@example.com"], "cc": ["cc1@example.com", "cc2@example.com"]},
        {"username": "Alice Tan", "goh": "Mr. John Lam", "to": ["recipient2@example.com"], "cc": ["cc3@example.com"]},
    ],
    "CompanyB": [
        {"username": "John Doe", "goh": "Mr. John Lam", "to": ["recipient3@example.com"], "cc": ["cc4@example.com", "cc5@example.com"]},
        {"username": "Jane Smith", "goh": "Mr. John Lam", "to": ["recipient4@example.com"], "cc": ["cc6@example.com"]},
    ]
}

# Set the email title once
email_title = "Important Announcement"

# Set email sender
email_sender = "sender1@example.com"

# Email content template
email_template = """
From: {email_sender}
To: {to_list}
Cc: {cc_list}
Subject: {email_title}

Dear {username},

Abc {goh}

Best Regards,
Your Company
"""

# Base directory to save company folders
base_dir = "output"

# Generate .eml files
for company, entries in data.items():
    # Create a directory for each company
    company_dir = os.path.join(base_dir, company)
    os.makedirs(company_dir, exist_ok=True)

    for entry in entries:
        # Convert lists of TO and CC emails to comma-separated strings
        to_list = ", ".join(entry.get("to", []))  # Handle cases where "to" might be missing
        cc_list = ", ".join(entry.get("cc", []))  # Handle cases where "cc" might be missing

        email_content = email_template.format(
            username = entry["username"],
            goh = entry["goh"],
            email_sender = email_sender,
            to_list = to_list,
            cc_list = cc_list,
            email_title = email_title
        )

        
        # Define the .eml file name
        filename = f"{entry['username'].replace(' ', '_')}.eml"
        
        # Write the email content to the file in the company's folder
        file_path = os.path.join(company_dir, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(email_content)

        print(f"Generated: {file_path}")

print("All .eml files have been created successfully.")