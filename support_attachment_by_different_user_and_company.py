import os
import mimetypes
from email.message import EmailMessage

# Sample JSON data with multiple CC recipients grouped by company
data = {
    "CompanyA": [
        {"username": "Peter Chan", "goh": "Mr. John Lam", "to": ["recipient1@example.com"], "cc": ["cc1@example.com", "cc2@example.com"], "attachments": ["attachment/dummy.pdf"]},
        {"username": "Alice Tan", "goh": "Mr. John Lam", "to": ["recipient2@example.com"], "cc": ["cc3@example.com"], "attachments": ["attachment/dummy.pdf"]},
    ],
    "CompanyB": [
        {"username": "John Doe", "goh": "Mr. John Lam", "to": ["recipient3@example.com"], "cc": ["cc4@example.com", "cc5@example.com"], "attachments": ["attachment/dummy.pdf"]},
        {"username": "Jane Smith", "goh": "Mr. John Lam", "to": ["recipient4@example.com"], "cc": ["cc6@example.com"], "attachments": ["attachment/dummy.pdf"]},
    ]
}

# Set the email title and sender
email_title = "Important Announcement"
email_sender = "sender1@example.com"

# Email content template
email_body_template = """Dear {username},

This is message template {goh} for testing.

Best Regards,
Peter Chan
"""

# Generate .eml files with attachments
for company, recipients in data.items():
    # Create directory for company
    company_dir = os.path.join("output", company)
    os.makedirs(company_dir, exist_ok=True)

    for entry in recipients:
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

        # Add attachments if provided
        for file_path in entry.get("attachments", []):
            if os.path.exists(file_path):  # Check if file exists
                mime_type, _ = mimetypes.guess_type(file_path)
                mime_type = mime_type or "application/octet-stream"

                with open(file_path, "rb") as f:
                    file_data = f.read()
                    file_name = os.path.basename(file_path)

                email_msg.add_attachment(file_data, maintype=mime_type.split('/')[0], subtype=mime_type.split('/')[1], filename=file_name)
            else:
                print(f"Warning: Attachment '{file_path}' not found. Skipping...")

        # Define the .eml file path
        filename = os.path.join(company_dir, f"{entry['username']}.eml")

        # Write email content to file
        with open(filename, "wb") as file:
            file.write(email_msg.as_bytes())

        print(f"Generated: {filename}")

print("All .eml files have been created successfully.")
