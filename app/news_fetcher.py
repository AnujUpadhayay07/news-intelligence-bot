import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_news(query: str, days_back: int = 7, max_articles: int = 10) -> list[dict]:
    """
    Fetch latest news articles for a given query.
    Returns a list of cleaned article dictionaries.
    """
    
    # Calculate date range
    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")
    
    params = {
        "q": query,
        "from": from_date,
        "to": to_date,
        "language": "en",
        "sortBy": "publishedAt",    # latest first
        "pageSize": max_articles,
        "apiKey": NEWS_API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "ok":
            print(f"NewsAPI error: {data.get('message', 'Unknown error')}")
            return []
        
        articles = []
        for article in data["articles"]:
            # Skip articles with missing content
            if not article.get("title") or not article.get("description"):
                continue
            
            # Clean and structure each article
            cleaned = {
                "title": article["title"],
                "source": article["source"]["name"],
                "published_at": article["publishedAt"][:10],  # just the date
                "description": article.get("description", ""),
                "content": article.get("content", article.get("description", "")),
                "url": article.get("url", "")
            }
            articles.append(cleaned)
        
        print(f"✅ Fetched {len(articles)} articles for query: '{query}'")
        return articles
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching news: {e}")
        return []


def format_articles_for_embedding(articles: list[dict]) -> list[str]:
    """
    Convert articles into text chunks ready for embedding.
    Each chunk = title + source + date + content
    """
    chunks = []
    for article in articles:
        chunk = f"""
Title: {article['title']}
Source: {article['source']}
Date: {article['published_at']}
Content: {article['content']}
URL: {article['url']}
        """.strip()
        chunks.append(chunk)
    return chunks


def format_articles_for_context(articles: list[dict]) -> str:
    """
    Format articles into a single string to pass to LLM as context.
    """
    context = ""
    for i, article in enumerate(articles, 1):
        context += f"""
Article {i}:
Title: {article['title']}
Source: {article['source']}
Date: {article['published_at']}
Content: {article['content']}
---
        """
    return context.strip()


# Quick test — run this file directly to test
if __name__ == "__main__":
    articles = fetch_news("Nvidia", days_back=7, max_articles=5)
    
    if articles:
        print("\n--- Sample Article ---")
        print(f"Title: {articles[0]['title']}")
        print(f"Source: {articles[0]['source']}")
        print(f"Date: {articles[0]['published_at']}")
        print(f"Content preview: {articles[0]['content'][:200]}...")
    else:
        print("No articles found.")