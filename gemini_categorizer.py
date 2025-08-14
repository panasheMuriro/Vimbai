from google import genai
from scrappers.zimeye import get_articles as get_zimeye_articles
from scrappers.pindula import get_articles as get_pindula_articles
from scrappers.new_zimbabwe import get_articles as get_newzimbabwe_articles
from scrappers.news_day import get_articles as get_newsday_articles
from scrappers.news_dze_zimbabwe import get_articles as get_newsdze_articles
import json
import os

# Set your Google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDwNf-aRo-BLGmjPcjngkdYro73RYGdXbw"


def categorize_articles():
    """Fetch articles from all sources and categorize using Gemini Flash Lite."""
    # Fetch articles
    print("Fetching articles from all sources...")
    zimeye_articles = get_zimeye_articles()
    pindula_articles = get_pindula_articles()
    newzimbabwe_articles = get_newzimbabwe_articles()
    newsday_articles = get_newsday_articles()
    newsdze_articles = get_newsdze_articles()

    all_articles = zimeye_articles + pindula_articles + newzimbabwe_articles + newsday_articles + newsdze_articles
    print(f"Total articles fetched: {len(all_articles)}")

    # Prepare summaries for prompt
    articles_for_prompt = [{"summary": a["summary"]} for a in all_articles]

    prompt = f"""
You are an AI assistant. I have a list of articles below, each with a summary. 
Please categorize these articles into **6 meaningful groups**. 
Return the output in JSON format with keys as category names and values as lists of article summaries.

Articles:
{json.dumps(articles_for_prompt, indent=2)}
"""

    client = genai.Client()

    response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt,
)
  
    categorized_text = response.text
    return categorized_text

if __name__ == "__main__":
    result = categorize_articles()
    print(result)
