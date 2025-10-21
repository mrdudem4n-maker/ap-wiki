# 🧠 Apollo Wiki — Transcript Summarization Pipeline (Ollama + Python)

This component converts long-form discussion transcripts into structured **Markdown bullet summaries** for integration into the Apollo Wiki knowledge base.  
It uses the local **Ollama** LLM server (running models like `mistral:7b`) via Python’s HTTP API.

---

## 📦 Overview

**Goal:**  
Feed large transcript `.txt` files into a local model (via `ollama serve`) and generate concise, timestamped bullet summaries formatted for Markdown.

**Example Output:**
```markdown
- (00:05:32, `911-nostalgia-ad5.md`) [[charlie_kirk]] disputes donor influence within [[tpusa]].
- (00:10:44) [[candace_owens]] releases screenshots of the group chat controversy.

🧰 Requirements
Tool	Version	Purpose
Python	≥3.9	Runs summarization script
Ollama	≥0.1.39	Hosts the local LLM
CUDA GPU	RTX 3060 + recommended	Enables fast inference
Model	mistral:7b	Default summarizer (balanced quality + speed)
⚙️ Setup Instructions
1. Clone / Navigate to Your Project
cd ~/apollo_wiki

2. Create Folders
mkdir -p transcripts summaries scripts

3. Install Dependencies
sudo apt update
sudo apt install python3 python3-pip -y
pip install requests

4. Pull the Model
ollama pull mistral:7b:q4_K_M

5. Start the Ollama Server

Run this in a dedicated terminal:

ollama serve


💡 Keep this terminal open while running summaries.
The API listens on http://localhost:11434.

🧠 6. Run the Summarizer

Place raw transcripts (plain text) into /transcripts:

transcripts/
 ├─ 911-nostalgia-ad5.txt
 ├─ owens-interview.txt
 └─ kirk-roundtable.txt


Then execute:

python3 scripts/summarize_transcript.py


This will:

Read each .txt file in /transcripts

Send its text to the local model via the Ollama API

Generate a Markdown summary

Save to /summaries/<filename>_summary.md

Example output:

summaries/
 └─ 911-nostalgia-ad5_summary.md

🧩 7. Script Details

The Python script (scripts/summarize_transcript.py) performs:

Request streaming from http://localhost:11434/api/generate

Chunking for long transcripts (>8 k tokens)

Structured Markdown output

Neutral tone with internal wikilinks

Excerpt:

MODEL = "mistral:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """You are the Apollo Summarizer.
Summarize this transcript into Markdown bullet points grouped by topic or timestamp.
Use [[wikilinks]] for names, keep a neutral tone, and output pure Markdown."""

🧾 Example CLI Test

Before running the script, you can test Ollama directly:

ollama run mistral:7b \
  -p "Summarize this transcript into bullet points: $(cat transcripts/911-nostalgia-ad5.txt)"

🧩 Troubleshooting
Problem	Likely Cause	Fix
Connection refused	Ollama server not running	Run ollama serve
Killed or CUDA error	Model too large for GPU	Use quantized version (:q4_K_M)
Truncated output	Default token limit	Add "options": {"num_predict": 4096} in API request
UTF-8 errors	Non-UTF text in transcript	Convert using iconv -f ISO-8859-1 -t UTF-8 file.txt > fixed.txt
🧭 Workflow Integration

After summaries are generated:

Move Markdown files into /summaries/

Run validate_topic_index.py to update topic_index.json

Commit both files to the Apollo Wiki GitHub repo

🧩 Future Model Options
Model	Description	Command
phi3:14b	More narrative, human-like summaries	ollama pull phi3:14b:q4_K_M
llama3.1:70b	Wikipedia-grade detail, slower	ollama pull llama3.1:70b:q4_K_M
✅ Example Full Workflow
# 1. Start local model
ollama serve

# 2. Run summarizer
python3 scripts/summarize_transcript.py

# 3. Validate and commit
python3 scripts/validate_topic_index.py
git add summaries/ topic_index.json
git commit -m "Add new transcript summaries"
git push
