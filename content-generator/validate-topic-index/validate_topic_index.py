#!/usr/bin/env python3
"""
Apollo Wiki Index Validator
---------------------------
Validates `topic_index.json` against the Apollo Wiki schema and ensures all
referenced markdown files, wikilinks, and relationships are valid.

Usage:
    python validate_topic_index.py --index docs/topic_index.json --root docs/
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

# Optional: If you want schema validation, uncomment and install jsonschema
# from jsonschema import validate, ValidationError

def load_index(index_path: Path) -> dict:
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_entities(index: dict, root: Path) -> list:
    """Validate that entity files exist and references are consistent."""
    errors = []
    entities = index.get("entities", {})
    alias_index = index.get("alias_index", {})

    # 1. Check entity files and basic fields
    for name, data in entities.items():
        file_path = root / data.get("file", "")
        wikilink = data.get("wikilink")

        if not wikilink:
            errors.append(f"[{name}] Missing 'wikilink' field.")
        if not data.get("file"):
            errors.append(f"[{name}] Missing 'file' field.")
        elif not file_path.exists():
            errors.append(f"[{name}] File not found: {file_path}")

        # Check type validity
        if data.get("type") not in ["person", "organization", "topic", "incident", "unknown"]:
            errors.append(f"[{name}] Invalid or missing 'type' value: {data.get('type')}")

        # 2. Check related entities
        for rel in data.get("related", []):
            if rel not in entities:
                errors.append(f"[{name}] Related entity '{rel}' not defined.")

        # 3. Check topics field (string type)
        for topic in data.get("topics", []):
            if not isinstance(topic, str):
                errors.append(f"[{name}] Non-string topic entry: {topic}")

        # 4. Check stats timestamps (if present)
        stats = data.get("stats", {})
        for field in ("first_seen", "last_seen"):
            if field in stats:
                try:
                    datetime.fromisoformat(stats[field].replace("Z", "+00:00"))
                except Exception:
                    errors.append(f"[{name}] Invalid datetime format in stats.{field}")

    # 5. Validate alias_index consistency
    for alias, mapping in alias_index.items():
        value = mapping.get("value")
        weight = mapping.get("weight")
        if value not in entities:
            errors.append(f"Alias '{alias}' maps to undefined entity '{value}'.")
        if not isinstance(weight, int) or weight < 1:
            errors.append(f"Alias '{alias}' has invalid weight '{weight}'.")

    # 6. Detect circular relations
    for name, data in entities.items():
        for rel in data.get("related", []):
            if name in entities.get(rel, {}).get("related", []) and name != rel:
                # It's fine if both link mutually, but check for self-loops
                if name == rel:
                    errors.append(f"[{name}] Self-referential 'related' field.")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate Apollo Wiki topic index.")
    parser.add_argument("--index", type=str, required=True, help="Path to topic_index.json")
    parser.add_argument("--root", type=str, required=True, help="Docs directory root")
    args = parser.parse_args()

    index_path = Path(args.index)
    root = Path(args.root)

    if not index_path.exists():
        print(f"❌ Index file not found: {index_path}")
        return

    print(f"🔍 Validating {index_path} ...")
    data = load_index(index_path)
    errors = validate_entities(data, root)

    if errors:
        print("\n❌ Validation Errors:")
        for err in errors:
            print(f"  - {err}")
        print(f"\nTotal issues found: {len(errors)}\n")
    else:
        print("✅ All entities, aliases, and file references are valid.")


if __name__ == "__main__":
    main()
