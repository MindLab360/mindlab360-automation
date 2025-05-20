import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# ইউটিউব API এর জন্য প্রয়োজনীয় তথ্য
CLIENT_ID = os.getenv("YT_CLIENT_ID")
CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")

# OAuth2 credentials setup
creds = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    token_uri='https://oauth2.googleapis.com/token',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# YouTube API client তৈরি
youtube = build('youtube', 'v3', credentials=creds)

# ভিডিও আপলোড সেটিংস
request_body = {
    'snippet': {
        'categoryId': '27',
        'title': 'Test Upload from GitHub Actions',
        'description': 'Uploaded using YouTube API and GitHub Actions',
        'tags': ['Test', 'GitHub', 'YouTube']
    },
    'status': {
        'privacyStatus': 'private',  # অথবা 'public', 'unlisted'
    }
}

mediaFile = MediaFileUpload('video.mp4', chunksize=-1, resumable=True, mimetype='video/mp4')

# ভিডিও আপলোড এক্সিকিউশন
upload_request = youtube.videos().insert(
    part="snippet,status",
    body=request_body,
    media_body=mediaFile
)

response = upload_request.execute()
print("Video uploaded. Video ID:", response.get("id"))
