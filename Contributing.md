# 🤝 Contributing to Apollo Wiki

Thank you for your interest in improving the Apollo Wiki!  
This guide explains **how to create, edit, and submit Markdown articles** either through GitHub’s web interface or locally using Git.

---

## ✍️ 1. Creating or Editing an Article (GUI Method)

1. Visit the repo on GitHub:  
   👉 https://github.com/yourusername/apollo-wiki
2. Click the **“docs/”** folder.
3. Choose **Add file → Create new file**.
4. Name your file (for example):  `docs/philosophy/causality.md`

`5. Write your article in **Markdown**.   Use wiki-style internal links like: ```markdown See also: [[Determinism]] and [[Abrahamic Theories]]`

6. Scroll down and click **“Commit changes”**.
    
    - Add a short commit message (e.g. “Add causality article”)
        
    - Choose **Commit directly to the main branch** or **Create a new branch** and **Open pull request** if you prefer review.
        

The site will rebuild automatically within ~1 minute after your commit.

---

## 🧰 2. Local Development (Git CLI Method)

If you’re comfortable with Git:
```bash
#1. Fork and clone the repository
git clone https://github.com/yourusername/apollo-wiki.git cd apollo-wiki

# 2. (Optional) Create a new branch
git checkout -b add-causality-article

# 3. Create or edit Markdown files in /docs
nano docs/philosophy/causality.md
# or use VS Code / any editor

# 4. Preview locally
pip install -r requirements.txt mkdocs serve

# 5. Commit and push your changes
git add . 
git commit -m "Add causality article" 
git push origin add-causality-article
```

Then open a Pull Request on GitHub.  
Once merged, your article appears automatically on the live site.

---

## 🧱 3. Markdown & Formatting Guidelines

- **Headings:** Use `#`, `##`, `###` for sections.
- **Internal links:** Use `[[Page Name]]` syntax (handled by `mkdocs-ezlinks-plugin`).
- **External links:** Standard Markdown `[label](url)`.
- **Images:** Place images in `docs/assets/images/` and embed as:
```
![Caption](../assets/images/example.png)
```
- Admonitions (info boxes):
```markdown
!!! note
    This is a highlighted note.
```
- Tags (optional):
Add front-matter metadata:
```markdown
---
tags:
  - philosophy
  - metaphysics
---
```


---

## 🧩 4. Page Organization

- Each top-level folder under `/docs` acts as a **wiki category** (e.g., `philosophy`, `history`, `science`).
- Each `.md` file is a separate article.
- The navigation sidebar is generated automatically using `mkdocs-awesome-pages-plugin`, but you can control ordering by adding a `.pages` file in any folder.
    

Example `.pages`:
```yaml
title: Philosophy
arrange:
  - causality.md
  - determinism.md
```

---

## 🧠 5. Need Help?

- **Local preview issues:** Run `mkdocs serve -v` to view build logs.
- **Broken links:** Make sure your filenames and link text match (case-sensitive).
- **Questions:** Open a [GitHub Issue](https://github.com/yourusername/apollo-wiki/issues/new).

---

Thank you for helping build the Apollo Wiki!

---

## ✅ Summary

| File | Purpose |
|------|----------|
| **README.md** | For project owners / deployers — setup, run, deploy |
| **CONTRIBUTING.md** | For writers — how to submit Markdown articles via GitHub or locally |
