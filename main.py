from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import base64

app = FastAPI()

# Allow CORS for local dev and Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = 587
EMAIL_HOST_USER = "medistatsolutions@gmail.com"
EMAIL_HOST_PASSWORD = "shmh sjjr pwsx zupv"
EMAIL_FROM = "medistatsolutions@gmail.com"

@app.post("/send-invoice-attachment/")
async def send_invoice_attachment(
    to_email: str = Body(...),
    to_name: str = Body(...),
    subject: str = Body("Your Medistat Invoice"),
    pdf_base64: str = Body(...),
    filename: str = Body("invoice.pdf")
):
    print("Query params:", {
        "to_email": to_email,
        "to_name": to_name,
        "subject": subject,
        "filename": filename
    })
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM
        msg["To"] = to_email
        msg["Subject"] = subject
        body = f"""
        <p>Dear {to_name},</p>
        <p>Your invoice is attached as a PDF.</p>
        <p>Thank you for choosing Medistat Solutions.</p>
        <br/>
        <p>Best regards,<br/>Medistat Solutions Team</p>
        """
        msg.attach(MIMEText(body, "html"))
        # Decode PDF and attach
        pdf_bytes = base64.b64decode(pdf_base64)
        part = MIMEApplication(pdf_bytes, _subtype="pdf")
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(EMAIL_FROM, to_email, msg.as_string())
        return {"status": "sent"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to send email: {e}"}) 