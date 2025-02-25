# import smtplib
# import csv
# from datetime import datetime
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import os

# # SMTP configuration
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 465
# EMAIL = os.environ.get('USER_EMAIL')
# PASSWORD = os.environ.get('USER_PASSWORD')

# # Debug environment variables
# if not EMAIL or not PASSWORD:
#     print("Error: USER_EMAIL or USER_PASSWORD environment variable not set.")
#     exit(1)

# # Load SSL data from CSV
# CSV_FILE = "ssl_data.csv"

# def send_email(domain, expiry_date, days_remaining):
#     """Send an email alert about SSL certificate expiry."""
#     subject = f"SSL Certificate Expiry Alert for {domain}"
#     body = f"""
#     Dear Webmaster,

#     This is an automated alert to notify you of the upcoming SSL certificate expiration for the following domain:

#     - Domain Name: {domain}
#     - SSL Expiry Date: {expiry_date}

#     Please take action to renew the SSL certificate before it expires. Here are the details:

#     1. If (1 month or less) remains for expiry, please prioritize this renewal.
#     2. If (2 weeks or less) remains for expiry, this is critical and requires immediate action.

#     If you have already renewed the SSL certificate, please update our records.

#     Best regards,
#     Nigeria Risk Index Automation Bot
#     """

#     # Prepare email
#     msg = MIMEMultipart()
#     msg['From'] = EMAIL
#     msg['To'] = "webmaster@riskcontrolnigeria.com"
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         # Send the email using SMTP_SSL
#         with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
#             server.login(EMAIL, PASSWORD)
#             server.sendmail(EMAIL, "webmaster@riskcontrolnigeria.com", msg.as_string())
#         print(f"Email sent successfully for {domain}")
#     except Exception as e:
#         print(f"Failed to send email for {domain}: {e}")

# def check_ssl_dates():
#     """Check SSL expiry dates and send alerts."""
#     today = datetime.now()
#     try:
#         with open(CSV_FILE, 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 domain = row['Domain Name']
#                 expiry_date = datetime.strptime(row['Next Due Date'], "%b %d, %Y")
#                 days_remaining = (expiry_date - today).days

#                 print(f"Checking {domain}: {days_remaining} days remaining (expiry: {expiry_date})")

#                 # Send email for specific conditions
#                 if days_remaining in [30, 13, 6]:
#                     print(f"Sending email for {domain} (days remaining: {days_remaining})")
#                     send_email(domain, expiry_date.strftime("%b %d, %Y"), days_remaining)
#     except FileNotFoundError:
#         print(f"CSV file '{CSV_FILE}' not found. Please check the file path.")
#     except Exception as e:
#         print(f"An error occurred: {e}")


# if __name__ == "__main__":
#     # Test SMTP Authentication
#     try:
#         with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
#             server.login(EMAIL, PASSWORD)
#             print("SMTP Authentication successful!")
#     except Exception as e:
#         print(f"SMTP Authentication failed: {e}")
#         exit(1)

#     check_ssl_dates()

import pandas as pd
import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# ================================
# 🔹 1. Read Excel File from SharePoint
# ================================

# OneDrive/SharePoint direct download link
EXCEL_URL = "https://riskcontrolacademy-my.sharepoint.com/:x:/g/personal/webmaster_riskcontrolnigeria_com/Ef_739nav8lNhfrMNawxVzQB6KSVvbeNVa0l-HjawRtzpQ?download=1"

try:
    # Read Excel file from SharePoint
    df = pd.read_excel(EXCEL_URL, engine="openpyxl")

    # Convert "Next Due Date" and "SSL Expiry Date" to datetime format
    df["Next Due Date"] = pd.to_datetime(df["Next Due Date"], errors="coerce")
    df["SSL Expiry Date"] = pd.to_datetime(df["SSL Expiry Date"], errors="coerce")

    # Print sample data to confirm
    print("✅ Successfully loaded SSL data:")
    print(df[["Domain Name", "Next Due Date", "SSL Expiry Date"]].head())

except Exception as e:
    print(f"❌ Failed to load Excel file: {e}")
    exit(1)

# ================================
# 🔹 2. SMTP Email Configuration
# ================================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL = os.environ.get('USER_EMAIL')
PASSWORD = os.environ.get('USER_PASSWORD')

if not EMAIL or not PASSWORD:
    print("❌ Error: USER_EMAIL or USER_PASSWORD environment variable not set.")
    exit(1)

# ================================
# 🔹 3. Function to Send Email Alerts
# ================================
def send_email(domain, expiry_date, days_remaining):
    """Send an email alert about SSL certificate expiry."""
    subject = f"🚨 SSL Certificate Expiry Alert: {domain}"
    body = f"""
    Dear Webmaster,

    This is an automated alert to notify you of the upcoming SSL certificate expiration for the following domain:

    🔹 **Domain Name:** {domain}
    🔹 **SSL Expiry Date:** {expiry_date}
    🔹 **Days Remaining:** {days_remaining}

    Please take action to renew the SSL certificate **before it expires**.

    🔴 **Urgency Levels:**
    - If **30 days or less** remain, please prioritize renewal.
    - If **13 days or less** remain, action is critical.
    - If **6 days or less** remain, immediate renewal is required.

    If you have already renewed the SSL certificate, please update our records.

    Best regards,  
    **Nigeria Risk Index Automation Bot**
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = "webmaster@riskcontrolnigeria.com"
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, "webmaster@riskcontrolnigeria.com", msg.as_string())
        print(f"✅ Email sent successfully for {domain}")
    except Exception as e:
        print(f"❌ Failed to send email for {domain}: {e}")

# ================================
# 🔹 4. Check SSL Expiry Dates and Send Alerts
# ================================
today = datetime.now()

for _, row in df.iterrows():
    domain = row["Domain Name"]
    expiry_date = row["Next Due Date"]

    # Check if expiry date exists
    if pd.notna(expiry_date):
        days_remaining = (expiry_date - today).days
        print(f"🔍 Checking {domain}: {days_remaining} days remaining (Expiry: {expiry_date.strftime('%b %d, %Y')})")

        # Send alerts only when necessary
        if days_remaining in [30, 13, 6]:
            print(f"🚨 Sending SSL expiry alert for {domain} (Expires in {days_remaining} days)")
            send_email(domain, expiry_date.strftime("%b %d, %Y"), days_remaining)

print("✅ SSL expiry check completed.")
