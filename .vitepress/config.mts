import { defineConfig } from "vitepress"

export default defineConfig({
  title: "AI Knowledge Wiki",
  description: "Public Markdown Wiki built with VitePress and Decap CMS",
  base: "/",

  themeConfig: {
    nav: [
      { text: "Home", link: "/" },
      { text: "Getting Started", link: "/getting-started" },
      { text: "Examples", link: "/examples/ai-feedback-loop" },
    ],

    sidebar: [
      {
        text: "Wiki",
        items: [
          { text: "Getting Started", link: "/getting-started" },
          { text: "AI Feedback Loop", link: "/examples/ai-feedback-loop" },
        ],
      },
    ],

    editLink: {
      pattern:
        "https://github.com/YOUR_GITHUB_USERNAME/markdown-wiki/edit/main/docs/:path",
      text: "Edit this page",
    },

    socialLinks: [
      {
        icon: "github",
        link: "https://github.com/YOUR_GITHUB_USERNAME/markdown-wiki",
      },
    ],
  },
})
