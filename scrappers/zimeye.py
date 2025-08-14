import requests
from bs4 import BeautifulSoup
from .summarize import summarize_text  
# import nltk
# nltk.download('punkt')

BASE_URL = "https://www.zimeye.net/category/national/"
TARGET_DATE = "13 August, 2025"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


def get_filtered_posts():
    resp = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    posts = soup.select(".post_cat")

    filtered = []
    for post in posts:
        date_tag = post.select_one(".pst_date")
        if date_tag and date_tag.get_text(strip=True).endswith(TARGET_DATE):
            link_tag = post.find("a", href=True)
            if link_tag:
                filtered.append(link_tag["href"])
    return list(set(filtered))  # remove duplicates

def scrape_post(url):
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")

    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
    content_div = soup.select_one(".page-content")
    content = content_div.get_text("\n", strip=True) if content_div else ""

    # Summarize content with 5 sentences (~0.5 ratio equivalent)
    summary = summarize_text(content, ratio=0.3) if len(content.split()) > 50 else content

    return {
        "url": url,
        "title": title,
        # "content": content,
        "summary": summary
    }

def get_articles():
    """
    Scrapes all articles for the given TARGET_DATE,
    returns a list of dicts with url, title, content, summary.
    """
    articles = []
    print("Starting to get Zimeye articles")
    links = get_filtered_posts()
    for link in links:
        articles.append(scrape_post(link))
    print(f"Done getting {len(articles)} articles from Zimeye")
    return articles

if __name__ == "__main__":
    articles = get_articles()
    print(f"Found {len(articles)} articles from {TARGET_DATE}\n")
    for art in articles:
        print(f"Title: {art['title']}\nURL: {art['url']}\n")
        print(f"Summary:\n{art['summary'] or art['content'][:300]}...\n{'-'*80}\n")
