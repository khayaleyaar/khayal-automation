import os
import json
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
VIDEO_FILE = "sample.mp4"

def get_service():
    # Load credentials JSON from environment
    creds_data = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    creds = None

    # If token.pickle exists in repo root, use it
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # Refresh or run console flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(creds_data, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

def upload():
    if not os.path.exists(VIDEO_FILE):
        raise FileNotFoundError(f"{VIDEO_FILE} missing in repo root")
    service = get_service()
    request = service.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Daily Islamic Short – Test",
                "description": "15-sec auto-upload via GitHub Actions",
                "tags": ["islamic", "shorts", "automation"]
            },
            "status": {"privacyStatus": "private"}
        },
        media_body=MediaFileUpload(VIDEO_FILE, chunksize=-1, resumable=True)
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
    print("Uploaded video ID:", response["id"])

if __name__ == "__main__":
    upload()
