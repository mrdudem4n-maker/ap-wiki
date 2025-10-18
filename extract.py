import os
import re
import json
import time
import html
import requests
from bs4 import BeautifulSoup

# === CONFIG ===
BASE_URL = "https://radixjournal.substack.com"
ARCHIVE_URL = f"{BASE_URL}/api/v1/archive"
OUT_TXT_DIR = "transcripts"
OUT_JSON_DIR = "transcripts_raw"
INDEX_FILE = "transcripts_index.json"

os.makedirs(OUT_TXT_DIR, exist_ok=True)
os.makedirs(OUT_JSON_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# === HELPERS ===

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
        html_text = requests.get(post_url, headers=HEADERS, timeout=10).text
        # Find the transcription.json URL up to any quote or backslash
        match = re.search(r"https://substackcdn\.com/video_upload/[^\s\"\\]+transcription\.json[^\s\"\\]+", html_text)
        if not match:
            return None
        raw_url = match.group(0)
        clean_url = re.sub(r"\\+$", "", html.unescape(raw_url.strip()))
        return clean_url
    except Exception as e:
        print(f"Error fetching {post_url}: {e}")
        return None


def download_transcript(transcript_url):
    """Download and return both JSON and text transcript."""
    try:
        clean_url = transcript_url.strip().rstrip("\\")
        res = requests.get(clean_url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        data = res.json()
        # Convert to plain text for AI digestion
        text = " ".join(seg.get("text", "") for seg in data).strip()
        return data, text
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error {e.response.status_code} for {transcript_url}")
        return None, None
    except Exception as e:
        print(f"Error downloading transcript {transcript_url}: {e}")
        return None, None


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
            data, text = download_transcript(t_url)

            if data and text:
                # Save raw JSON
                json_path = os.path.join(OUT_JSON_DIR, f"{slug}.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                # Save clean text
                txt_path = os.path.join(OUT_TXT_DIR, f"{slug}.txt")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)

                print(f"💾 Saved: {txt_path} and {json_path}")

                results.append({
                    "title": title,
                    "slug": slug,
                    "post_url": post_url,
                    "transcript_url": t_url,
                    "text_path": txt_path,
                    "json_path": json_path,
                })
            else:
                print("⚠️ Transcript found but could not be downloaded.")
        else:
            print("❌ No transcript found.")

        time.sleep(1)  # polite delay

    # Write index file
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Completed! Index saved to {INDEX_FILE}")


if __name__ == "__main__":
    main()
