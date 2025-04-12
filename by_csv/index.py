import os
import mimetypes
from email.message import EmailMessage
import pandas as pd

# Read CSV file
csv_file = "sample.csv"
df = pd.read_csv(csv_file)

# Convert CSV data to the required dictionary format
data = {}
for org, group in df.groupby("Organization"):
    employees = []
    for _, row in group.iterrows():
        employee = {
            "username": row["Name"],
            "goh": row["Goh"],
            "to": row["Email"].split(",") if pd.notna(row["Email"]) else [],
            "cc": row["CC"].split(",") if pd.notna(row["CC"]) else []
        }
        employees.append(employee)
    data[org] = employees

# Set the email title and sender
email_title = "Important Announcement"
email_sender = "sender1@example.com"

# List of attachment file paths
attachments = ["../attachment/dummy.pdf"]  # Add more file paths to this list for multiple attachments

# Email content template
email_body_template = """Dear {username},

This is message template {goh} for testing.

Best Regards,  
Peter Chan
"""

# Generate .eml files with attachments and organize them by company
for company, employees in data.items():
    # Create directory for the company
    company_dir = os.path.join("output", company)
    os.makedirs(company_dir, exist_ok=True)
    
    for entry in employees:
        # Create email message
        email_msg = EmailMessage()
        email_msg["From"] = email_sender
        email_msg["To"] = ", ".join(entry.get("to", []))
        email_msg["Cc"] = ", ".join(entry.get("cc", []))
        email_msg["Subject"] = email_title

        # Set email body
        email_body = email_body_template.format(
            username=entry["username"],
            goh=entry["goh"]
        )
        email_msg.set_content(email_body)

        # Add attachments
        for attachment_path in attachments:
            if os.path.exists(attachment_path):  # Check if file exists
                mime_type, _ = mimetypes.guess_type(attachment_path)
                mime_type = mime_type or "application/octet-stream"

                with open(attachment_path, "rb") as f:
                    file_data = f.read()
                    file_name = os.path.basename(attachment_path)

                email_msg.add_attachment(file_data, maintype=mime_type.split('/')[0], subtype=mime_type.split('/')[1], filename=file_name)
            else:
                print(f"Warning: Attachment '{attachment_path}' not found. Skipping...")

        # Define the .eml file path
        filename = os.path.join(company_dir, f"{entry['username']}.eml")

        # Write email content to file
        with open(filename, "wb") as file:
            file.write(email_msg.as_bytes())

        print(f"Generated: {filename}")

print("All .eml files have been created successfully.")