import os, json, requests, textwrap

MODEL = "mistral:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """You are the Apollo Summarizer.

Summarize each transcript into concise Markdown bullet points grouped by topic or timestamp.
Rules:
- Use [[wikilinks]] for people, organizations, incidents, and themes.
- Keep neutral, factual tone.
- Include filename and timestamp when given.
- One bullet = one idea or event.
- Output pure Markdown, no prose intro."""

def call_ollama(prompt: str) -> str:
    response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt}, stream=True)
    output = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            output += data.get("response", "")
    return output

def summarize_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # optional: chunk if > 7000 tokens (~10k words)
    chunks = textwrap.wrap(text, 10000)
    combined = ""
    for i, chunk in enumerate(chunks, 1):
        print(f"→ Processing chunk {i}/{len(chunks)} for {filepath}")
        prompt = f"{SYSTEM_PROMPT}\n\nTranscript chunk {i}:\n{chunk}"
        combined += call_ollama(prompt) + "\n\n"

    return combined.strip()

if __name__ == "__main__":
    os.makedirs("summaries", exist_ok=True)
    for file in os.listdir("transcripts"):
        if not file.endswith(".txt"):
            continue
        path = os.path.join("transcripts", file)
        print(f"Summarizing {file}...")
        summary = summarize_file(path)
        out_path = os.path.join("summaries", file.replace(".txt", "_summary.md"))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"✅ Saved to {out_path}")
