# 🏛️ Apollo Wiki

**Apollo Wiki** is a collaborative, Markdown-based knowledge base built with [MkDocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.  
It organizes curated discussions, transcripts, and ideas into a navigable, wiki-style site powered by free GitHub Pages hosting.

---

## 🌐 Live Site
**https://yourusername.github.io/apollo-wiki**

---

## 🧩 Features
- 🗂 **Flat-file Markdown**: every article is a `.md` file under `/docs/`
- 🔗 **Wiki-style linking** via `[[Page Name]]` (handled by [`mkdocs-ezlinks-plugin`](https://github.com/orbifx/mkdocs-ezlinks-plugin))
- 🔍 **Instant search**, sidebar navigation, and light/dark themes (Material)
- 🕓 **Last-updated timestamps** from Git commits
- 🖼️ **Clickable lightbox images** (Glightbox)
- 🚀 **Automatic deploy** to GitHub Pages using GitHub Actions

---

## ⚙️ Project Structure

apollo-wiki/  
├── docs/ # All wiki articles live here  
│ ├── index.md # Homepage  
│ ├── abrahamic_theories.md  
│ └── philosophy/  
│ ├── causality.md  
│ └── determinism.md  
├── mkdocs.yml # MkDocs configuration  
└── .github/workflows/  
└── deploy.yml # GitHub Pages deployment workflow


---

## 🧱 Local Development

### 1. Install prerequisites
```bash
python3 -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the local server

`mkdocs serve`

Visit [http://localhost:8000](http://localhost:8000)

### 3. Build the static site

`mkdocs build`

---

## 🚀 Deployment (GitHub Pages)

This repository is configured for automatic deployment:

- Push any commit to the **`main`** branch.
- GitHub Actions runs MkDocs and publishes to the `gh-pages` branch.
- The site updates at  
    **https://yourusername.github.io/apollo-wiki**

If you need to deploy manually:

`mkdocs gh-deploy --force`

---

## 🧩 Requirements.txt Reference

`mkdocs-material mkdocs-ezlinks-plugin mkdocs-git-revision-date-localized-plugin mkdocs-awesome-pages-plugin mkdocs-glightbox pymdown-extensions`

---

## 🤝 Contributing

If you’d like to add or edit an article, please read  
👉 CONTRIBUTING.md
