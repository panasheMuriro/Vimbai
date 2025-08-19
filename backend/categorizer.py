from google import genai
from scrappers.zimeye import get_articles as get_zimeye_articles
from scrappers.pindula import get_articles as get_pindula_articles
from scrappers.new_zimbabwe import get_articles as get_newzimbabwe_articles
from scrappers.news_day import get_articles as get_newsday_articles
from scrappers.news_dze_zimbabwe import get_articles as get_newsdze_articles
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from utils.firebase import post_to_firestore
import json
import os
import re
import json5

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY", "")


def summarize_text(text: str, sentence_count: int = 2) -> str:
    """Summarize text to a few sentences using Sumy LSA."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()

    total_sentences = len(parser.document.sentences)
    if total_sentences == 0:
        return text

    summary_count = min(sentence_count, total_sentences)
    summary_sentences = summarizer(parser.document, summary_count)
    return " ".join(str(sentence) for sentence in summary_sentences)




def safe_json_loads(text: str):
    """Parse loose JSON from Gemini safely using json5."""
    # Extract the first { ... } block
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in the text")
    json_text = match.group()
    
    return json5.loads(json_text)

def categorize_articles():
    """Categorize articles using Gemini Flash Lite with 2-sentence summaries."""
    print("Fetching articles from all sources...")
    all_articles = (
        # get_zimeye_articles() +
        get_pindula_articles()
        # get_newzimbabwe_articles() +
        # get_newsday_articles() +
        # get_newsdze_articles()
    )
    print(f"Total articles fetched: {len(all_articles)}")

    # Generate short summaries for Gemini input
    articles_for_prompt = []
    for a in all_articles:
        short_summary = summarize_text(a["summary"], sentence_count=2)
        articles_for_prompt.append({
            "title": a.get("title") or a.get("heading"),
            "short_summary": short_summary
        })

    prompt = f"""
You are an AI assistant. I have a list of articles with their titles and very short summaries. 
Please categorize these articles into **3 meaningful groups**. 
Return the output in JSON format with keys as category names and values as lists of article titles.

Articles:
{json.dumps(articles_for_prompt, indent=2)}
"""

    print("Starting Gemini categorizer")
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
    )

    # categorized_text = response.text
   
    raw_text = response.text
    print(raw_text)
    categorized_dict = safe_json_loads(raw_text)
    # categorized_dict = json.loads(categorized_text)

    # Map back to original articles for full info
    title_to_article = { (a.get("title") or a.get("heading")): a for a in all_articles }
    final_categorized = {}
    for category, titles in categorized_dict.items():
        final_categorized[category] = [title_to_article[t] for t in titles if t in title_to_article]

    return final_categorized

if __name__ == "__main__":
    categorized_articles = categorize_articles()
    for cat, articles in categorized_articles.items():
        print(f"Category: {cat}")
        for a in articles:
            print(f"- {a.get('title') or a.get('heading')}")
        print("\n")
        
    serializable_data = {
        category: [dict(article) for article in articles]
        for category, articles in categorized_articles.items()
    }
    
    print("Starting posting to Firebase")

    # Push to Firestore
    post_to_firestore(serializable_data)
