import cohere
from scrappers.zimeye import get_articles as get_zimeye_articles
from scrappers.pindula import get_articles as get_pindula_articles
import json

COHERE_API_KEY="KrUb4uw2lwaK1H4EItptK49y4bd0ubAYgi29E9jC"

def categorize_articles():
    zimeye_articles = get_zimeye_articles()
    pindula_articles = get_pindula_articles()
    all_articles = zimeye_articles + pindula_articles
    # all_articles = zimeye_articles
    articles_for_prompt = [
        {"summary": a["summary"]} for a in all_articles
    ]

    prompt = f"""
You are an AI assistant. I have a list of articles below, each with a title and summary. 
Please categorize these articles into **5 meaningful groups**. 
Return the output in JSON format with keys as category names and values as lists of article summaries.

Articles:
{json.dumps(articles_for_prompt, indent=2)}
"""

    co = cohere.ClientV2(COHERE_API_KEY)

    response = co.chat(
        model="command-xlarge-nightly",  # chat-compatible model
        messages=[{"role": "user", "content": prompt}],
        # max_tokens=600,
        # temperature=0.3
    )

    # The model output
    categorized_text = response.message.content
    return categorized_text

if __name__ == "__main__":
    result = categorize_articles()
    print(result)
