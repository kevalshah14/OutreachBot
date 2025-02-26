import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(subject, body, to_email):
    sender_email = os.environ.get('GOOGLE_EMAIL')  # Get sender email from environment variable
    sender_password = os.environ.get('GOOGLE_EMAIL_PASSWORD')  # Get sender email password from environment variable
    smtp_server = "smtp.gmail.com"  # SMTP server for Gmail
    smtp_port = 587  # SMTP port for Gmail

    msg = MIMEMultipart()  # Create a multipart message
    msg['From'] = sender_email  # Set the sender email
    msg['To'] = to_email  # Set the recipient email
    msg['Subject'] = subject  # Set the email subject

    msg.attach(MIMEText(body, 'plain'))  # Attach the email body

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)  # Login to the email account
        server.sendmail(sender_email, to_email, msg.as_string())  # Send the email
        print(f"Email sent to {to_email}")  # Print confirmation

def send_bulk_emails(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            to_email = row[0]  # Get the recipient email from the CSV
            subject = "Your Subject Here"  # Set the email subject
            body = row[1]  # Get the email body from the CSV
            send_email(subject, body, to_email)  # Send the email

send_bulk_emails('emails.csv')  # Call the function with the CSV file
