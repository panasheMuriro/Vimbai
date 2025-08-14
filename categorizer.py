# from ollama import Client

# client = Client(host="http://localhost:11434")  

# prompt =""


# response = client.chat(
#     model="llama3.2:latest",
#     messages=[
#         {"role": "user", "content": prompt}
#     ],
# )

# # The model output
# print(response)



# combined_scraper.py
# categorizer.py

import json
from ollama import Client

# Import scraper functions
from scrappers.zimeye import get_articles as get_zimeye_articles
from scrappers.pindula import get_articles as get_pindula_articles


def categorize_articles():
    """
    Fetch articles from all scrapers and categorize them into 5 groups using LLaMA 3.2.
    Returns the raw model output (JSON string with categories).
    """
    # 1️⃣ Fetch articles
    zimeye_articles = get_zimeye_articles()
    pindula_articles = get_pindula_articles()
    all_articles = zimeye_articles + pindula_articles
    print("Starting to categorizer with ollama")

    # 2️⃣ Prepare prompt
    articles_for_prompt = [
        {"summary": a["summary"]} for a in all_articles
    ]

    prompt = f"""
You are an AI assistant. I have a list of articles below, each with a title and summary. 
Please categorize these articles into **5 meaningful groups**. 
Return the output in JSON format with keys as category names and values as lists of article titles.

Articles:
{json.dumps(articles_for_prompt, indent=2)}
"""

    # 3️⃣ Initialize Ollama client
    client = Client(host="http://localhost:11434")  

    # 4️⃣ Get categorization from LLaMA 3.2
    response = client.chat(
        model="llama3.2:latest",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return response


# Example usage when running this file directly
if __name__ == "__main__":
    result = categorize_articles()
    print(result)
