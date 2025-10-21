# 🧩 Apollo Wiki — Topic Index Validator

**File:** `validate_topic_index.py`  
**Purpose:** Validate the structure, integrity, and consistency of your `topic_index.json` file used by the Apollo Wiki system.

---

## 🚀 Overview

This utility ensures that:

- Every **entity** in `topic_index.json` follows the Apollo Wiki schema.
- All referenced **Markdown files** exist within `/docs/`.
- All **aliases** map to defined canonical entities.
- **Relationships** (`related`, `topics`) and **timestamps** are valid.
- The file is safe for use with **Obsidian + MkDocs (ezlinks)**.

It’s designed to catch broken links or schema drift **before publishing** or committing changes.

---

## 🧠 Requirements

- Python 3.8+
- (Optional) `jsonschema` package for deeper schema validation:
    `pip install jsonschema`
---

## 🧭 Usage

`python validate_topic_index.py --index docs/topic_index.json --root docs/`
### Example Output

#### ✅ Successful Validation

`🔍 Validating docs/topic_index.json ... ✅ All entities, aliases, and file references are valid.`

#### ❌ With Errors

`🔍 Validating docs/topic_index.json ... ❌ Validation Errors:   - [Charlie Kirk] File not found: docs/people/charlie-kirk.md   - Alias 'TP' maps to undefined entity 'TPUSA'  Total issues found: 2`

---

## 🧰 Arguments

|Flag|Description|Example|
|---|---|---|
|`--index`|Path to the `topic_index.json` file.|`--index docs/topic_index.json`|
|`--root`|Root folder containing your markdown docs.|`--root docs/`|

---

## ⚙️ What It Checks

|Validation|Description|
|---|---|
|**File existence**|Verifies that every `file` field points to an actual `.md` file.|
|**Wikilink consistency**|Ensures all entities have a `wikilink` in underscore_case.|
|**Related integrity**|Checks that each `related` reference exists in `entities`.|
|**Alias integrity**|Ensures each alias maps to a valid canonical entity and has `weight >= 1`.|
|**Datetime format**|Validates ISO8601 timestamps (`2025-10-18T09:15:00Z`).|
|**Self/circular references**|Detects improper loops or self-references in `related`.|

---

## 🧪 Recommended Workflow

1. **Run locally** before each commit:
    `python validate_topic_index.py --index docs/topic_index.json --root docs/`
2. **Integrate with CI/CD** (e.g., GitHub Actions) to prevent invalid topic maps from being merged.
3. **Use alongside Obsidian and MkDocs** to guarantee cross-platform link integrity.

---

## 🧩 Notes

- The script supports both **hyphen-case filenames** (`charlie-kirk.md`) and **underscore_case wikilinks** (`[[charlie_kirk]]`), matching Apollo Wiki’s hybrid linking design.
- Future versions may include automatic **alias weight updates**, **conflict logging**, and **topic graph visualization**.
