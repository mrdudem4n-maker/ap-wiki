#!/usr/bin/env python3
"""
Apollo Wiki — Transcript Summarizer (Bullet + Topic Index)
----------------------------------------------------------
Summarizes discussion transcripts into Markdown bullet points
and updates topic_index.json with discovered entities.
"""

import os
import json
import re
import textwrap
import requests
from tqdm import tqdm

# === Configuration ===
MODEL = "mistral:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"
TRANSCRIPTS_DIR = "transcripts"
SUMMARIES_DIR = "summaries"
TOPIC_INDEX_PATH = "topic_index.json"
CHUNK_SIZE = 9000
MAX_OUTPUT_TOKENS = 1024

# === Prompt Template ===
SYSTEM_PROMPT = """You are the Apollo Summarizer.

Read the provided transcript text and return only concise Markdown bullet points.
Each bullet should describe one clear statement, question, or idea mentioned.

### Formatting rules
- Use one bullet per idea.
- Start each bullet with "-" followed by a space.
- If timestamps exist, include them in [HH:MM:SS] format.
- Identify real named entities (people, organizations, incidents, or themes) with [[wikilinks]].
- Never use generic words like "speaker", "guest", or "host".
- Skip greetings or filler.
- Output only the bullets, no introductions or explanations.

Example:
- [00:01:22] [[charlie_kirk]] discusses donor pressure at [[tpusa]].
- [00:04:58] [[candace_owens]] describes tensions with [[daily_wire]].
- [00:09:17] [[nick_fuentes]] comments on [[fbi]] involvement.
"""


# === Ollama API Call ===
def call_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "options": {"num_predict": MAX_OUTPUT_TOKENS}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
    except requests.exceptions.ConnectionError:
        raise SystemExit("❌ Cannot connect to Ollama. Run `ollama serve` first.")

    output = ""
    for line in response.iter_lines():
        if not line:
            continue
        data = json.loads(line)
        output += data.get("response", "")
    return output.strip()

# === Topic Index Helpers ===
def load_topic_index():
    """Load or initialize topic_index.json safely."""
    if not os.path.exists(TOPIC_INDEX_PATH):
        print("ℹ️ No existing topic_index.json found — creating a new one.")
        return {"entities": {}}

    try:
        with open(TOPIC_INDEX_PATH, "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:
                print("⚠️ topic_index.json is empty — reinitializing.")
                return {"entities": {}}
            return json.loads(data)
    except (json.JSONDecodeError, ValueError):
        print("⚠️ topic_index.json is invalid — backing up and resetting.")
        # backup the broken file
        os.rename(TOPIC_INDEX_PATH, TOPIC_INDEX_PATH + ".bak")
        return {"entities": {}}

def save_topic_index(index):
    """Safely save topic index with UTF-8 encoding."""
    tmp_path = TOPIC_INDEX_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, TOPIC_INDEX_PATH)

# Ignore generic or placeholder terms that aren't real entities
GENERIC_IGNORE = {
    "speaker", "speakers", "guest", "guests", "host", "hosts",
    "panelist", "panelists", "moderator", "interviewer", "audience",
    "participant", "participants", "Discussion Summary"
}


def is_valid_entity(entity_name: str) -> bool:
    normalized = entity_name.strip().lower()
    if normalized in GENERIC_IGNORE:
        return False
    if len(normalized) < 3:
        return False
    return True


def update_topic_index(index, summary_text, source_file):
    """
    Update topic_index.json using wikilinks and, if missing,
    inferred entities from capitalized names.
    """

    # 1️⃣ extract explicit wikilinks
    wikilinks = re.findall(r"\[\[([^\]]+)\]\]", summary_text)

    # 2️⃣ extract timestamps
    timestamps = re.findall(r"\[(\d{2}:\d{2}:\d{2})\]", summary_text)

    # 3️⃣ if no wikilinks found, infer from capitalized words
    if not wikilinks:
        # find proper names like "Nick Fuentes", "Charlie Kirk", "FBI"
        inferred = re.findall(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+|[A-Z]{2,})\b", summary_text)
        wikilinks = [w.strip() for w in inferred if len(w) > 2]
        print(f"ℹ️ Inferred entities from text: {wikilinks}")

    for topic in wikilinks:
        topic_key = topic.strip().lower().replace(" ", "_")
        # Skip junk or generic placeholders
        if not is_valid_entity(topic_key):
            continue

        entity = index["entities"].setdefault(topic_key, {"weight": 0, "sources": []})
        entity["weight"] += 1

        # attach all timestamps from current summary for now
        for ts in timestamps or ["unknown"]:
            entity["sources"].append({"file": source_file, "timestamp": ts})

    return index

# === Summarization Logic ===
def summarize_file(filepath: str, topic_index: dict) -> str:
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    chunks = textwrap.wrap(text, CHUNK_SIZE)
    summary = f"# Discussion Summary\n_Source: {filename}_\n\n"

    for i, chunk in enumerate(tqdm(chunks, desc=f"Summarizing {filename}")):
        chunk_prompt = f"{SYSTEM_PROMPT}\n\nTranscript chunk {i+1}/{len(chunks)}:\n\n{chunk}"
        chunk_summary = call_ollama(chunk_prompt)

    # Normalize common bullet markers (*, —, •) to "-"
    normalized = []
    for line in chunk_summary.splitlines():
        clean = line.strip()
        if not clean:
            continue
        if clean.startswith(("-", "*", "•")):
            normalized.append(clean.replace("*", "-").replace("•", "-"))
        elif re.match(r"^\[?\d{2}:\d{2}:\d{2}\]?", clean):
            normalized.append(f"- {clean}")  # prefix timestamp-only lines
        # fallback: lines with verbs or wikilinks are probably bullets
        elif "[[" in clean or re.search(r"\bdiscusses|mentions|criticizes|supports|questions\b", clean):
            normalized.append(f"- {clean}")

        # keep only clean bullets
        filtered = "\n".join(normalized)
        if not filtered.strip():
            print(f"⚠️ Warning: No bullet points detected in chunk {i+1} — printing raw model output for inspection:\n{chunk_summary[:400]}...\n")
            filtered = chunk_summary  # fallback to raw output
        summary += filtered + "\n"

    # update topic index with this summary’s entities
    update_topic_index(topic_index, summary, filename)
    return summary.strip()

# === Main ===
def main():
    os.makedirs(SUMMARIES_DIR, exist_ok=True)
    topic_index = load_topic_index()

    files = [f for f in os.listdir(TRANSCRIPTS_DIR) if f.endswith(".txt")]
    if not files:
        print("⚠️ No transcript files found in /transcripts")
        return

    for file in files:
        input_path = os.path.join(TRANSCRIPTS_DIR, file)
        output_path = os.path.join(SUMMARIES_DIR, file.replace(".txt", "_summary.md"))
        print(f"\n🧠 Processing: {file}")

        try:
            summary = summarize_file(input_path, topic_index)
        except Exception as e:
            print(f"❌ Error processing {file}: {e}")
            continue

        with open(output_path, "w", encoding="utf-8") as out:
            out.write(summary)
        print(f"✅ Saved summary → {output_path}")

    save_topic_index(topic_index)
    print(f"\n🗂  topic_index.json updated with {len(topic_index['entities'])} entities.")
    print("🏁 All transcripts summarized successfully!")

if __name__ == "__main__":
    main()
