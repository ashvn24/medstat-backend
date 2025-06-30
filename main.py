from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import base64
import requests

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

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz3UNV_x43LieC8YonKjKi9bQoVGNsytKfmnjOg22QiBn_crryURzpU66AvDySUQehg-A/exec"

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

@app.post("/update-testimonial")
async def update_testimonial(data: dict = Body(...)):
    row = data.get("row", 0)
    print("row", row)
    if row <= 1:
        return JSONResponse(status_code=200, content={"error": "Cannot update header row"})
    params = {
        "action": "update",
        "row": row,
        "Feedback": data.get("Feedback", ""),
        "Suggestions": data.get("Suggestions", ""),
        "Name": data.get("Name", ""),
        "Email": data.get("Email", "")
    }
    try:
        print(f"[UPDATE] Sending params to Apps Script: {params}")
        response = requests.get(GOOGLE_SCRIPT_URL, params=params)
        print(f"[UPDATE] Apps Script response: {response.status_code} {response.text}")
        return {"status": "success", "apps_script_response": response.text}
    except Exception as e:
        print(f"[UPDATE] Error: {e}")
        return JSONResponse(status_code=500, content={"error": f"Failed to update testimonial: {e}"})

@app.post("/delete-testimonial")
async def delete_testimonial(data: dict = Body(...)):
    params = {
        "action": "delete",
        "row": data["row"]
    }
    try:
        print(f"[DELETE] Sending params to Apps Script: {params}")
        response = requests.get(GOOGLE_SCRIPT_URL, params=params)
        print(f"[DELETE] Apps Script response: {response.status_code} {response.text}")
        return {"status": "success"}
    except Exception as e:
        print(f"[DELETE] Error: {e}")
        return JSONResponse(status_code=500, content={"error": f"Failed to delete testimonial: {e}"}) 