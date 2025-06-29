# Medistat Backend (FastAPI)

This backend provides an API to upload PDF invoices to Google Drive and return a shareable link.

## Setup

1. **Create a Google Cloud Project & Service Account**
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.
   - Enable the Google Drive API for your project.
   - Create a Service Account and download the JSON credentials file.
   - Share your target Google Drive folder with the service account email (give Editor access).

2. **Place Credentials**
   - Save the credentials file as `backend/credentials.json` (or set the `GOOGLE_CREDS_PATH` env variable).

3. **(Optional) Set Folder ID**
   - To upload to a specific folder, set the `GOOGLE_DRIVE_FOLDER_ID` environment variable.

4. **Install dependencies**
   - Activate the virtual environment:
     ```
     backend-venv\Scripts\activate
     ```
   - Install requirements (already done if you followed setup):
     ```
     pip install fastapi uvicorn python-multipart google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
     ```

5. **Run the server**
   ```
   uvicorn backend.main:app --reload --port 8000
   ```

## API

### POST `/upload-invoice/`
- **Body:** `multipart/form-data` with a `file` field (PDF)
- **Response:** `{ "link": "https://drive.google.com/file/d/FILE_ID/view?usp=sharing" }`

---

## CORS
CORS is enabled for all origins for development. Restrict in production as needed. 