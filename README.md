<div align="center">

**Real-time AI news analysis · RAG · Contradiction Detection · Conversational Memory**

[![Live Demo](https://img.shields.io/badge/🌐%20Live%20Demo-Open%20App-00d4ff?style=for-the-badge)](https://news-intelligence-bot-bbatdxapctcydfbh.eastus-01.azurewebsites.net)
[![GitHub](https://img.shields.io/badge/GitHub-AnujUpadhayay07-181717?style=for-the-badge&logo=github)](https://github.com/AnujUpadhayay07/news-intelligence-bot)

---

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-latest-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![Azure OpenAI](https://img.shields.io/badge/Azure_OpenAI-GPT--4-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6B35?style=flat-square)
![NewsAPI](https://img.shields.io/badge/NewsAPI-Real--time-E74C3C?style=flat-square)
![Azure App Service](https://img.shields.io/badge/Azure_App_Service-B1_Linux-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## 🌐 Live App

```
https://news-intelligence-bot-bbatdxapctcydfbh.eastus-01.azurewebsites.net
```

> ✅ Status: **Running** · East US · Python 3.12 · Linux · B1 Basic

---

## ✨ What It Does

| Feature | Description |
|---|---|
| 📰 **Real-Time News** | Fetches live articles from NewsAPI for any query |
| 🧠 **RAG Pipeline** | Embeds articles in ChromaDB, retrieves top-K by semantic similarity |
| 🤖 **GPT-4 Answers** | Grounded answers from Azure OpenAI based on real articles |
| ⚡ **Contradiction Detection** | Detects when different sources contradict each other |
| 💬 **Conversational Memory** | Follow-up questions answered in context of chat history |
| 📊 **Source Citations** | Every answer includes source URLs, dates, and relevance scores |
| 🎯 **Sentiment Analysis** | Positive / Negative / Neutral sentiment per response |

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend (app/api.py)    │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌───────────────┐    ┌──────────────────────┐
│  news_fetcher │    │     rag_chain.py      │
│  (NewsAPI)    │    │                      │
│  10 articles  │───▶│  1. Embed articles   │
└───────────────┘    │  2. Store in Chroma  │
                     │  3. Retrieve top-K   │
                     │  4. GPT-4 generates  │
                     │  5. Add to memory    │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼───────────┐
                     │ contradiction_detector│
                     │ Compare sources →    │
                     │ flag conflicts       │
                     └──────────────────────┘
```

---

## 🗂️ Project Structure

```
news-intelligence-bot/
│
├── 📁 app/
│   ├── __init__.py
│   ├── api.py                     # FastAPI routes
│   ├── rag_chain.py               # LangChain RAG pipeline + memory
│   ├── news_fetcher.py            # NewsAPI integration
│   └── contradiction_detector.py  # Cross-source analysis
│
├── 📁 prompts/
│   └── rag_prompt.py              # System prompt for GPT-4
│
├── 📁 static/
│   └── index.html                 # Frontend UI (single file)
│
├── 📁 .github/workflows/
│   └── main_news-intelligence-bot.yml  # GitHub Actions CI/CD
│
├── requirements.txt
├── .env                           # ⚠️ Never commit!
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| 🐍 **Runtime** | Python 3.12 | Language |
| ⚡ **Backend** | FastAPI + Uvicorn | REST API server |
| 🦜 **AI Framework** | LangChain | RAG orchestration |
| 🤖 **LLM** | Azure OpenAI GPT-4 | Answer generation |
| 🔢 **Embeddings** | Azure OpenAI text-embedding | Vector creation |
| 🗄️ **Vector DB** | ChromaDB | Semantic search |
| 📰 **News Source** | NewsAPI | Real-time articles |
| ☁️ **Hosting** | Azure App Service B1 | Cloud deployment |
| 🔄 **CI/CD** | GitHub Actions | Auto-deploy on push |

---

## 🚀 Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/AnujUpadhayay07/news-intelligence-bot.git
cd news-intelligence-bot
```

### 2. Create virtual environment

```bash
# Mac/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

```env
# NewsAPI
NEWSAPI_KEY=your_newsapi_key_here

# Azure OpenAI
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your_gpt4_deployment_name
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your_embedding_deployment_name
AZURE_OPENAI_API_VERSION=2024-02-01
```

### 5. Run the app

```bash
python -m app.api
```

Visit → **http://localhost:8000** 🎉

---

## 🔑 Environment Variables

| Variable | Description | Where to Get |
|---|---|---|
| `NEWSAPI_KEY` | NewsAPI access key | [newsapi.org](https://newsapi.org/register) |
| `AZURE_OPENAI_KEY` | Azure OpenAI resource key | Azure Portal → OpenAI → Keys |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | Azure Portal → OpenAI → Overview |
| `AZURE_OPENAI_DEPLOYMENT` | GPT-4 deployment name | Azure AI Studio → Deployments |
| `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` | Embedding model name | Azure AI Studio → Deployments |
| `AZURE_OPENAI_API_VERSION` | API version string | Use: `2024-02-01` |

---

## 🔁 RAG Pipeline (Step by Step)

```
1. 🙋 User asks a question
        ↓
2. 📰 NewsAPI fetches 10 latest relevant articles
        ↓
3. 🔢 Azure OpenAI Embeddings converts articles → vectors
        ↓
4. 🗄️ Vectors stored in ChromaDB
        ↓
5. 🔍 Top-K articles retrieved via cosine similarity
        ↓
6. 🧠 Articles + chat history → GPT-4 via LangChain prompt
        ↓
7. ✍️  GPT-4 generates grounded answer
        ↓
8. 💬 Answer saved to LangChain memory
        ↓
9. ⚡ Contradiction detector compares sources
        ↓
10. 📤 Answer + sources + contradictions → frontend
```

---

## 🔌 API Endpoints

### `GET /`
Serves the frontend UI (`static/index.html`)

---

### `POST /analyze`

Runs the full RAG pipeline for a news query.

**Request:**
```json
{
  "question": "What is happening with US-Iran relations?",
  "top_k": 5
}
```

**Response:**
```json
{
  "success": true,
  "answer": "According to recent articles from Reuters and HuffPost...",
  "sources": [
    {
      "title": "Article title",
      "source": "Reuters",
      "date": "2026-04-12",
      "url": "https://reuters.com/...",
      "relevance": 0.87
    }
  ],
  "articles_used": 5,
  "contradictions": {
    "contradictions_found": true,
    "contradictions": [
      {
        "topic": "Duration of US-Iran conflict",
        "severity": "low",
        "source1": "WBUR",
        "claim1": "Ongoing with no timeline",
        "source2": "The Intercept",
        "claim2": "Stretched into second month"
      }
    ],
    "summary": "1 contradiction found"
  }
}
```

---

## ☁️ Azure Deployment

### Resources

| Resource | Value |
|---|---|
| 🗂️ Resource Group | `rg-news-bot` |
| 📋 App Name | `news-intelligence-bot` |
| 📍 Region | East US |
| 🐧 OS | Linux |
| 🐍 Runtime | Python 3.12 |
| 💰 SKU | B1 Basic (1.75 GB RAM) |
| 🔗 Deployment | GitHub Actions |

### Startup Command

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000
```

### CI/CD Flow

```
git push main
    → GitHub Actions triggered
    → Build + install all packages
    → Deploy to Azure App Service
    → App live ✅
```

---

## 📦 requirements.txt

```txt
fastapi
uvicorn
python-dotenv
langchain
langchain-openai
langchain-chroma
langchain-community
chromadb
pysqlite3-binary
newsapi-python
pydantic
openai
```

---

## 👨‍💻 Author

**Anuj Upadhayay**

[![GitHub](https://img.shields.io/badge/GitHub-AnujUpadhayay07-181717?style=flat-square&logo=github)](https://github.com/AnujUpadhayay07)
[![BIT Mesra](https://img.shields.io/badge/BIT_Mesra-BCA_2024-0078D4?style=flat-square)](https://www.bitmesra.ac.in)

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

**Built with ❤️ · Powered by Azure OpenAI · Deployed on Azure App Service**

⭐ **Star this repo if you found it useful!**

</div>
