import smtplib
import csv
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "rcsnbc@gmail.com"
PASSWORD = "USER_PASSWORD"  # Replace with your email password

# Load SSL data from CSV
CSV_FILE = "ssl_data.csv"

def send_email(domain, hosted_location, expiry_date, days_remaining):
    subject = f"SSL Certificate Expiry Alert for {domain}"
    body = f"""
    Dear Webmaster,

    This is an automated alert to notify you of the upcoming SSL certificate expiration for the following domain:

    - **Domain Name**: {domain}
    - **Hosted Location**: {hosted_location}
    - **SSL Expiry Date**: {expiry_date}

    Please take action to renew the SSL certificate before it expires. Here are the details:

    1. If **1 month or less** remains for expiry, please prioritize this renewal.
    2. If **2 weeks or less** remains for expiry, this is critical and requires immediate action.

    If you have already renewed the SSL certificate, please update our records.

    Best regards,
    Nigeria Risk Index Automation Bot
    Email: rcsnbc@gmail.com
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = "nofiumoruf17@gmail.com"
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, "nofiumoruf17@gmail.com", msg.as_string())
        print(f"Email sent for {domain}")
    except Exception as e:
        print(f"Failed to send email for {domain}: {e}")

def check_ssl_dates():
    today = datetime.now()
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            domain = row['Domain Name']
            hosted_location = row['Hosted Location']
            expiry_date = datetime.strptime(row['Next Due Date'], "%b %d, %Y")
            days_remaining = (expiry_date - today).days

            if days_remaining == 30 or days_remaining == 14:
                send_email(domain, hosted_location, expiry_date.strftime("%b %d, %Y"), days_remaining)

if __name__ == "__main__":
    check_ssl_dates()