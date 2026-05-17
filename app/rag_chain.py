import os
from dotenv import load_dotenv

from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory

from app.news_fetcher import fetch_news
from app.contradiction_detector import detect_contradictions
from prompts.rag_prompt import SYSTEM_PROMPT

load_dotenv()

# ── Azure OpenAI clients ──────────────────────────────────────────
embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0.1
)

# ── ChromaDB via LangChain ────────────────────────────────────────
vectorstore = Chroma(
    collection_name="news_langchain",
    embedding_function=embeddings,
    persist_directory="vector_store"
)

# ── Conversation Memory ───────────────────────────────────────────
memory = ChatMessageHistory()

# ── Prompt Template with Memory ───────────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT + """

You also have access to the conversation history below.
Use it to understand follow-up questions and maintain context.
For example if user asks "what about their CEO?" refer back to
the company they previously asked about.
"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", """
Here are the latest news articles relevant to the query:

{context}

---

User Question: {question}

Answer based strictly on the articles above and conversation history.
""")
])


def format_docs(docs: list[Document]) -> str:
    """Format LangChain documents into context string."""
    context = ""
    for i, doc in enumerate(docs, 1):
        meta = doc.metadata
        context += f"""
Article {i}:
Title: {meta.get('title', 'Unknown')}
Source: {meta.get('source', 'Unknown')}
Date: {meta.get('date', 'Unknown')}
Content: {doc.page_content}
---
"""
    return context.strip()


def fetch_and_store(query: str, days_back: int = 7, max_articles: int = 10):
    """Fetch news → convert to LangChain Documents → store in Chroma."""
    print(f"\n📰 Fetching news for: '{query}'")
    articles = fetch_news(query, days_back=days_back, max_articles=max_articles)

    if not articles:
        print("❌ No articles found.")
        return []

    docs = []
    for article in articles:
        doc = Document(
            page_content=f"""
Title: {article['title']}
Source: {article['source']}
Date: {article['published_at']}
Content: {article['content']}
            """.strip(),
            metadata={
                "title": article["title"],
                "source": article["source"],
                "date": article["published_at"],
                "url": article["url"],
                "query": query
            }
        )
        docs.append(doc)

    print(f"🔢 Embedding {len(docs)} articles with LangChain...")
    vectorstore.add_documents(docs)
    print(f"✅ Stored {len(docs)} articles in vector store!")
    return articles


def retrieve_articles(query: str, top_k: int = 5):
    """Semantic search with relevance scores."""
    print(f"\n🔍 Retrieving relevant articles for: '{query}'")
    docs_with_scores = vectorstore.similarity_search_with_relevance_scores(
        query, k=top_k
    )
    print(f"✅ Retrieved {len(docs_with_scores)} articles!")
    for doc, score in docs_with_scores:
        print(f"   → [{round(score, 3)}] {doc.metadata.get('source')} - {doc.metadata.get('title', '')[:50]}...")
    return docs_with_scores


def answer_question(question: str, top_k: int = 5) -> dict:
    """
    Full LangChain RAG pipeline with memory:
    1. Fetch & store fresh news
    2. Retrieve relevant docs
    3. Generate grounded answer with chat history
    4. Save to memory
    5. Detect contradictions
    """
    print(f"\n🚀 LangChain RAG pipeline for: '{question}'")

    # Step 1 — Fetch & store fresh news
    fetch_and_store(question, days_back=7, max_articles=10)

    # Step 2 — Retrieve docs
    docs_with_scores = retrieve_articles(question, top_k=top_k)
    docs = [doc for doc, score in docs_with_scores]

    if not docs:
        return {
            "answer": "I don't have enough recent news to answer this accurately.",
            "sources": [],
            "articles_used": 0,
            "contradictions": {
                "contradictions_found": False,
                "contradictions": [],
                "summary": "No articles found"
            },
            "chat_history": []
        }

    # Step 3 — Build context
    context = format_docs(docs)

    # Step 4 — Get chat history
    chat_history = memory.messages
    print(f"💬 Chat history: {len(chat_history)} messages")

    # Step 5 — Run RAG chain with memory
    print(f"\n🤖 Running LangChain RAG chain with memory...")
    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({
        "context": context,
        "question": question,
        "chat_history": chat_history
    })
    print(f"✅ Answer generated!")

    # Step 6 — Save to memory
    memory.add_user_message(question)
    memory.add_ai_message(answer)

    # Step 7 — Format sources
    sources = []
    seen = set()
    for doc, score in docs_with_scores:
        title = doc.metadata.get("title", "")
        if title not in seen:
            seen.add(title)
            sources.append({
                "title": title,
                "source": doc.metadata.get("source", ""),
                "date": doc.metadata.get("date", ""),
                "url": doc.metadata.get("url", ""),
                "relevance": round(score, 3)
            })

    # Step 8 — Contradiction detection
    article_dicts = []
    for doc in docs:
        article_dicts.append({
            "source": doc.metadata.get("source", ""),
            "date": doc.metadata.get("date", ""),
            "content": doc.page_content
        })
    contradictions = detect_contradictions(article_dicts)

    # Step 9 — Format chat history for frontend
    history = []
    for msg in memory.messages:
        history.append({
            "role": "user" if isinstance(msg, HumanMessage) else "assistant",
            "content": msg.content
        })

    return {
        "answer": answer,
        "sources": sources,
        "articles_used": len(docs),
        "contradictions": contradictions,
        "chat_history": history
    }


def clear_memory():
    """Clear conversation memory."""
    memory.clear()
    print("🧹 Memory cleared!")


# Quick test
if __name__ == "__main__":
    result = answer_question("What is happening with OpenAI?")
    print("\n" + "="*60)
    print("ANSWER:")
    print("="*60)
    print(result["answer"])
    print(f"\nSources: {result['articles_used']}")
    print(f"Contradictions: {result['contradictions']['summary']}")