import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

CONTRADICTION_PROMPT = """
You are a fact-checking assistant. Analyze the following news articles and identify any contradictions or conflicting claims between them.

Look for:
1. Different numbers or statistics on the same topic
2. Conflicting statements about the same event
3. Different conclusions from the same data
4. Opposing claims about the same person, company, or event

Respond ONLY in this exact JSON format with no extra text:
{
  "contradictions_found": true or false,
  "contradictions": [
    {
      "topic": "what the contradiction is about",
      "source_a": "Source name 1",
      "claim_a": "what source 1 says",
      "source_b": "Source name 2", 
      "claim_b": "what source 2 says",
      "severity": "high" or "medium" or "low"
    }
  ],
  "summary": "one sentence summary of contradictions found, or 'No contradictions detected'"
}
"""

def detect_contradictions(articles: list[dict]) -> dict:
    """
    Compare articles against each other to find contradictions.
    """
    if len(articles) < 2:
        return {
            "contradictions_found": False,
            "contradictions": [],
            "summary": "Not enough articles to compare"
        }

    # Build article context
    context = ""
    for i, article in enumerate(articles, 1):
        context += f"""
Article {i} — {article['source']} ({article['date']}):
{article['content'][:500]}
---
"""

    print("\n🔍 Checking for contradictions...")

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": CONTRADICTION_PROMPT},
                {"role": "user", "content": f"Find contradictions in these articles:\n{context}"}
            ]
        )

        result = json.loads(response.choices[0].message.content)

        if result.get("contradictions_found"):
            print(f"⚠️  Found {len(result['contradictions'])} contradiction(s)!")
        else:
            print("✅ No contradictions found")

        return result

    except Exception as e:
        print(f"❌ Contradiction detection error: {e}")
        return {
            "contradictions_found": False,
            "contradictions": [],
            "summary": "Could not analyze contradictions"
        }