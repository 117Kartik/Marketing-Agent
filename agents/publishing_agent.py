import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_emails(file_path, campaign_data):
    try:
        df = pd.read_csv(file_path)

        emails = df["email"].dropna().tolist()

        sender_email = "your_email@gmail.com"
        sender_password = "your_app_password"  # NOT normal password

        subject = campaign_data["content"]["headline"]
        body = f"""
{campaign_data["content"]["description"]}

{campaign_data["content"]["cta"]}

{" ".join(campaign_data["content"]["hashtags"])}
"""

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for email in emails:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            server.sendmail(sender_email, email, msg.as_string())

        server.quit()

        return True, f"Sent to {len(emails)} users"

    except Exception as e:
        return False, str(e)