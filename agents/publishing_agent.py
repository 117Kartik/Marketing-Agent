import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

load_dotenv(os.path.join(ROOT_DIR, ".env"))


def send_emails(file_path, campaign_data):
    try:
        # Read file
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

        if "email" not in df.columns:
            return False, "File must contain 'email' column"

        emails = df["email"].dropna().tolist()

        # YOUR VERIFIED EMAIL
        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASS")
        if not sender_email or not sender_password:
            return False, "Email credentials not set in .env"

        subject = campaign_data["content"]["headline"]
        description = campaign_data["content"]["description"]
        cta = campaign_data["content"]["cta"]
        hashtags = " ".join(campaign_data["content"]["hashtags"])
        image_url = campaign_data.get("image_url", "")

        # HTML email
        html_body = f"""
        <html>
        <body style="font-family: Arial; background:#f4f4f4; padding:20px;">
            <div style="max-width:600px; margin:auto; background:white; padding:20px; border-radius:10px;">
                
                <h2>{subject}</h2>

                <p style="white-space: pre-line;">
                    {description}
                </p>

                {"<img src='" + image_url + "' style='width:100%; border-radius:10px;'/>" if image_url else ""}

                <p><b>{cta}</b></p>

                <p style="color:#2563eb;">{hashtags}</p>

            </div>
        </body>
        </html>
        """

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for email in emails:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = email
            msg["Subject"] = subject

            msg.attach(MIMEText(html_body, "html"))

            server.sendmail(sender_email, email, msg.as_string())

        server.quit()

        return True, f"Sent to {len(emails)} users"

    except Exception as e:
        return False, str(e)