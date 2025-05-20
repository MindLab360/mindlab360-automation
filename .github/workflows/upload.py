import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# Load environment variables from GitHub Secrets
CLIENT_ID = os.environ.get("YT_CLIENT_ID")
CLIENT_SECRET = os.environ.get("YT_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("YT_REFRESH_TOKEN")

# Automatically find the first .mp4 file in the root directory
video_file = None
for file in os.listdir("."):
    if file.lower().endswith(".mp4"):
        video_file = file
        break

if not video_file:
    raise FileNotFoundError("No .mp4 video file found in the repository root!")

# Video metadata
VIDEO_TITLE = "Auto Uploaded Video by GitHub Actions"
VIDEO_DESCRIPTION = "This video was uploaded using the YouTube Data API and GitHub Actions automation."
VIDEO_CATEGORY = "22"  # People & Blogs
VIDEO_PRIVACY = "private"  # Can be "private", "public", or "unlisted"

# Create credentials using refresh token
creds = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scopes=["https://www.googleapis.com/auth/youtube.upload"]
)

# Refresh access token
creds.refresh(Request())

# Build the YouTube API client
youtube = build("youtube", "v3", credentials=creds)

# Prepare the upload request
request_body = {
    "snippet": {
        "title": VIDEO_TITLE,
        "description": VIDEO_DESCRIPTION,
        "categoryId": VIDEO_CATEGORY,
    },
    "status": {
        "privacyStatus": VIDEO_PRIVACY
    }
}

media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/*")

# Upload the video
request = youtube.videos().insert(
    part="snippet,status",
    body=request_body,
    media_body=media
)

response = request.execute()
print("✅ Video uploaded successfully! Video ID:", response.get("id"))
