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
    # 1. Load the OAuth client secret JSON from GitHub secret
    client_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])

    # 2. Load existing token.pickle (refresh-token) if exists
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as f:
            token_dict = pickle.load(f)
        creds = Credentials.from_authorized_user_info(token_dict, SCOPES)
        if creds.expired:
            creds.refresh(Request())
            # save updated token
            with open("token.pickle", "wb") as f:
                pickle.dump(json.loads(creds.to_json()), f)
        return build("youtube", "v3", credentials=creds)

    # 3. If token.pickle missing → stop with clear message
    raise RuntimeError(
        "token.pickle missing! Run local script once to create it, then commit the file."
    )

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
