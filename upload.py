import os
import json
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
VIDEO_FILE = "sample.mp4"

def get_service():
    if not os.path.exists("token.pickle"):
        raise RuntimeError("token.pickle missing! Create it locally once.")
    with open("token.pickle", "rb") as f:
        token = pickle.load(f)
    creds = Credentials.from_authorized_user_info(token, SCOPES)
    if creds.expired:
        creds.refresh(Request())
        with open("token.pickle", "wb") as f:
            pickle.dump(json.loads(creds.to_json()), f)
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
            "status": {"privacyStatus": "public"}
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
