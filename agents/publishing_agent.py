import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # agents/
PROJECT_ROOT = os.path.dirname(BASE_DIR)               # marketing-agent/

env_path = os.path.join(PROJECT_ROOT, ".env")


load_dotenv(env_path)


cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET")
)


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
        hashtags = " ".join([f"#{tag.lstrip('#')}" for tag in campaign_data["content"]["hashtags"]])
        image_url = campaign_data.get("image_url", "")

        if image_url and "127.0.0.1" in image_url:
            try:
                filename = os.path.basename(image_url)

                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                IMAGE_DIR = os.path.join(BASE_DIR, "generated_images")

                local_path = os.path.join(IMAGE_DIR, filename)

                print("FINAL PATH:", local_path)
                print("FILE EXISTS:", os.path.exists(local_path))

                upload_result = cloudinary.uploader.upload(local_path)

                print("UPLOAD RESULT:", upload_result)

                image_url = upload_result.get("secure_url")

                print("FINAL CLOUD URL:", image_url)

            except Exception as e:
                print("CLOUDINARY ERROR:", str(e))

                # Upload to Cloudinary if local
                if image_url and "127.0.0.1" in image_url:
                    try:
                        local_path = image_url.split("/media/")[-1]
                        local_path = f"./media/{local_path}"
                        
                        upload_result = cloudinary.uploader.upload(local_path)
                        image_url = upload_result.get("secure_url")

                    except Exception as e:
                        print("Cloudinary upload failed:", str(e))

        # HTML email
        html_body = f"""
        <html>
        <body style="margin:0; padding:0; background:#f4f4f4; font-family:Arial;">

        <div style="max-width:600px; margin:auto; background:white; border-radius:10px; overflow:hidden;">

            <!--  HEADER / BRAND -->
            <div style="background:#111827; padding:15px; text-align:center;">
            <h1 style="color:white; margin:0;">{campaign_data.get("brand", "YourBrand")}</h1>
            </div>

            <!--  IMAGE -->
            {"<img src='" + image_url + "' style='width:100%; display:block;'/>" if image_url else ""}

            <!--  CONTENT -->
            <div style="padding:20px;">

            <h2 style="color:#111827; margin-bottom:10px;">
                {subject}
            </h2>

            <p style="color:#374151; line-height:1.6; white-space: pre-line;">
                {description}
            </p>

            <!--  CTA BUTTON -->
            <div style="text-align:center; margin:25px 0;">
                <a href="#"
                style="
                    background:#2563eb;
                    color:white;
                    padding:12px 25px;
                    text-decoration:none;
                    border-radius:6px;
                    font-weight:bold;
                    display:inline-block;
                ">
                {cta}
                </a>
            </div>

            <!--  HASHTAGS -->
            <p style="color:#2563eb; text-align:center;">
                {" ".join([f"#{tag.lstrip('#')}" for tag in campaign_data["content"]["hashtags"]])}
            </p>

            </div>

            <!--  FOOTER -->
            <div style="background:#f9fafb; padding:15px; text-align:center; font-size:12px; color:#6b7280;">
            You received this email because you are subscribed.<br/>
            © 2026 {campaign_data.get("brand", "YourBrand")}
            </div>

        </div>

        </body>
        </html>
        """

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        print("IMAGE URL USED IN EMAIL:", image_url)

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