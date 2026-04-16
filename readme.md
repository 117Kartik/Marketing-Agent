# AI Marketing Agent

An end-to-end AI-powered marketing system that generates ad campaigns, creates images, and sends personalized emails to users.

---

## Features

* AI-generated marketing campaigns (headline, description, CTA, hashtags)
* AI-generated product images
* Cloudinary integration for image hosting
* Bulk email sending via Gmail SMTP
* Upload Excel file with user emails
* Campaign history with image preview
* Campaign selection before publishing

---

## Tech Stack

* **Frontend:** React
* **Backend:** Django
* **AI APIs:** OpenAI / Groq
* **Database:** SQLite
* **Image Hosting:** Cloudinary
* **Email Service:** Gmail SMTP
* **Data Handling:** Pandas, OpenPyXL

---

## Setup Instructions

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd marketing-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup environment variables

Create a `.env` file in root:

```
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password

CLOUD_NAME=your_cloud_name
CLOUD_API_KEY=your_api_key
CLOUD_API_SECRET=your_api_secret
```

---

### 4. Run backend

```bash
cd backend
python manage.py runserver
```

---

### 5. Run frontend

```bash
npm install
npm run dev
```

---

## How it Works

1. Generate a campaign using AI
2. Image is created and stored locally
3. Image is uploaded to Cloudinary
4. Select campaign from history
5. Upload Excel file with emails
6. Send marketing emails with image + CTA

---

## Notes

* Excel file must contain an `email` column
* Uses Gmail App Password (not normal password)
* Images are hosted publicly for email compatibility

---

## Future Improvements

* Authentication system
* Campaign analytics dashboard
* Scheduled email campaigns
* Multi-user support

---

## Author

Kartik Chauhan
