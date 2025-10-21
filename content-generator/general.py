def summarize_transcript(file):
    transcript_text = read_txt(file)
    timestamps = read_json(file.replace('.txt', '.json'))
    canonical_terms = load_topic_index()
    
    # Split transcript into time-based segments
    segments = chunk_transcript(transcript_text, timestamps)

    all_bullets = []
    for segment in segments:
        prompt = build_prompt(segment, canonical_terms)
        summary = call_ollama(prompt)
        all_bullets.append(summary)

    write_markdown_summary(file, all_bullets)
    update_topic_index(file, all_bullets)
    validate_topic_index()
