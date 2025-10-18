import os
import re
import json
import time
import requests
import html
from bs4 import BeautifulSoup

BASE_URL = "https://radixjournal.substack.com"
ARCHIVE_URL = f"{BASE_URL}/api/v1/archive"
OUT_DIR = "transcripts"
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_archive():
    """Fetch the archive of all posts from the Substack channel."""
    print(f"Fetching archive from {ARCHIVE_URL} ...")
    res = requests.get(ARCHIVE_URL, headers=HEADERS)
    res.raise_for_status()
    posts = res.json()
    print(f"Found {len(posts)} posts.")
    return posts

def find_transcript_url(post_url):
    """Parse a post page to find a transcription.json URL."""
    try:
        html = requests.get(post_url, headers=HEADERS, timeout=10).text
        match = re.search(r"https://substackcdn\.com/video_upload/[^\"]+transcription\.json[^\"]*", html)
        return match.group(0) if match else None
    except Exception as e:
        print(f"Error fetching {post_url}: {e}")
        return None

import html

def find_transcript_url(post_url):
    """Parse a post page to find a transcription.json URL."""
    try:
        html_text = requests.get(post_url, headers=HEADERS, timeout=10).text
        # capture the full transcription.json URL up to a quote or backslash
        match = re.search(r"https://substackcdn\.com/video_upload/[^\s\"\\]+transcription\.json[^\s\"\\]+", html_text)
        if not match:
            return None
        raw_url = match.group(0)
        # clean stray backslashes or escape chars
        clean_url = html.unescape(raw_url.strip().rstrip("\\"))
        return clean_url
    except Exception as e:
        print(f"Error fetching {post_url}: {e}")
        return None

def download_transcript(transcript_url):
    """Download the transcript JSON and convert it to text."""
    try:
        # Sanitize again before request
        transcript_url = transcript_url.strip().rstrip("\\")
        res = requests.get(transcript_url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        data = res.json()
        text = " ".join(seg.get("text", "") for seg in data).strip()
        return text
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error {e.response.status_code} for {transcript_url}")
        print(f"→ Headers: {res.headers.get('content-type')}")
        return None
    except Exception as e:
        print(f"Error downloading transcript {transcript_url}: {e}")
        return None

def main():
    posts = get_archive()
    results = []

    for post in posts:
        slug = post.get("slug")
        title = post.get("title", "Untitled").replace("/", "-")
        post_url = f"{BASE_URL}/p/{slug}"

        print(f"\n🔍 Checking {title} ...")
        t_url = find_transcript_url(post_url)

        if t_url:
            print(f"✅ Found transcript: {t_url}")
            text = download_transcript(t_url)
            if text:
                filename = os.path.join(OUT_DIR, f"{slug}.txt")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(text)
                results.append({"title": title, "url": post_url, "transcript_url": t_url})
                print(f"💾 Saved transcript to {filename}")
        else:
            print("❌ No transcript found.")

        # Be polite to the server
        time.sleep(1)

    # Save index file
    with open("transcripts_index.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\n✅ All done. Transcripts saved in ./transcripts and index in transcripts_index.json")

if __name__ == "__main__":
    main()
