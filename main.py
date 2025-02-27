import json
import os

# Directory to save .eml files
output_dir = "eml_output"
os.makedirs(output_dir, exist_ok=True)

# Sample JSON data with multiple CC recipients
dataSet = [
    {"username": "Peter Chan", "goh": "Mr. John Lam", "to": ["recipient1@example.com"], "cc": ["cc1@example.com", "cc2@example.com"]},
    {"username": "Tom Cheung", "goh": "Mr. John Lam", "to": ["recipient1@example.com", "recipient2@example.com"], "cc": ["cc3@example.com", "cc4@example.com", "cc5@example.com"]},
]

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

This is message template {goh} for testing

Best Regards,
Peter Chan
"""

# Generate .eml files
for entry in dataSet:
    # Convert list of TO emails to a comma-separated string
    # Convert list of CC emails to a comma-separated string
    # Handle cases where "cc" might be missing
    to_list = ", ".join(entry.get("to", []))
    cc_list = ", ".join(entry.get("cc", []))
    
    # Replace placeholders in the email template using the format() method
    email_content = email_template.format(
        username = entry["username"],
        goh = entry["goh"],
        email_sender = email_sender,
        to_list = to_list,
        cc_list = cc_list,
        email_title = email_title
    )
    
    # Define the .eml file name
    filename = f"{output_dir}/{entry['username']}.eml"
    
    # Write the email content to the file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(email_content)

    print(f"Generated: {filename}")

print("All .eml files have been created successfully.")
