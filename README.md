# 🎨 SwagCraft — AI Merchandise Studio & Product Showcase

> **Build with Gemini · Track 3 Project**  
> An agentic merchandise studio that researches company breakthroughs, analyzes authentic brand aesthetics, and generates bespoke commercial studio product mockups.

---

## 💡 What is SwagCraft?

Most corporate swag is generic—a tiny logo slapped onto a cheap black item. **SwagCraft** changes that. 

Enter any company name, and SwagCraft:
1. 🔍 **Researches Latest Milestones**: Uses **Google Search Grounding** to identify the company's most recent major achievements, product launches, and authentic brand color palettes.
2. 🎨 **Designs Bespoke Merchandise**: Crafts custom physical products (chore jackets, custom mechanical keyboards, studio headphones, insulated thermal bottles, heavyweight hoodies) designed in the company's real brand colors with subtle commemorative edition accents.
3. 📸 **Commercial Studio Photography**: Generates photorealistic product mockup shots in single-color cyclorama studio environments using **Nano Banana 2 Lite** (`gemini-3.1-flash-lite-image`) on Vertex AI.
4. 💼 **Interactive Pitch UI**: Renders in a **Google Material Design 3** web experience with tactile carousel canvas selection, a horizontal showcase feed, and a one-click **"Send to boss"** proposal generator.

---

## 🏗️ Architecture & Google Cloud Building Blocks

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Agent Reasoning** | [Google ADK](https://google.github.io/adk-docs/) (`gemini-3.6-flash`) | Analyzes brand identity, orchestrates tools, and formulates design prompts |
| **Web Research** | Google Search Grounding | Discovers real company breakthroughs and signature color aesthetics |
| **Image Mockups** | Vertex AI (`gemini-3.1-flash-lite-image`) | High-resolution commercial studio product mockups with studio lighting |
| **Media Hosting** | Google Cloud Storage (GCS) | Public hosting and streaming of generated product visuals |
| **Web UI** | Material Design 3 (FastAPI + Vanilla JS) | Responsive, tactile interface with looping canvas picker and proposal sharing |

---

## 🗂️ Project Structure

```
.
├── swagcraft/                 # Core ADK agent service
│   ├── app/
│   │   ├── agent.py           # SwagCraft agent reasoning, grounding & instructions
│   │   └── tools.py           # Vertex AI image generation & GCS storage tools
│   ├── pyproject.toml         # Dependencies (uv-managed)
│   └── README.md
├── frontend/                  # Web application face
│   ├── main.py                # FastAPI server & ADK session proxy
│   └── static/
│       └── index.html         # Material 3 web app (carousel, showcase feed, modal)
├── project_brief.md           # Workshop project design brief
└── README.md                  # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- `uv` (recommended fast Python package manager)
- Google Cloud Project with Vertex AI and Google Cloud Storage APIs enabled
- Authenticated via `gcloud auth application-default login`

### Running Locally

1. **Install Dependencies**:
   ```bash
   cd swagcraft
   uv sync
   ```

2. **Set Environment Variables**:
   ```bash
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   export GOOGLE_CLOUD_LOCATION="global"
   ```

3. **Launch Application**:
   ```bash
   uv run python ../frontend/main.py
   ```

4. Open `http://localhost:8501` in your browser.

---

## 📄 License
Apache 2.0
