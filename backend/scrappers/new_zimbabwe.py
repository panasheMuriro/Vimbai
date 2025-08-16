import requests
from bs4 import BeautifulSoup
from .summarize import summarize_text  # Import reusable function


from utils.get_yesterday_date import get_yesterday_date

previous_date = get_yesterday_date('new_zimbabwe')

BASE_URL = "https://www.newzimbabwe.com/category/news/"
TARGET_DATE = previous_date
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def get_filtered_posts():
    """Fetches post links from the news category filtered by target date."""
    resp = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    posts = soup.select(".post-grid-content")

    filtered_links = set()
    for post in posts:
        footer = post.select_one(".post-grid-content-footer")
        if footer and TARGET_DATE in footer.get_text(strip=True):
            link_tag = post.find("a", href=True)
            if link_tag:
                filtered_links.add(link_tag["href"])

    return list(filtered_links)

def get_article_data(url):
    """Fetches title, body, and summary from an article URL."""
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.select_one(".post-title")
    body_tag = soup.select_one(".post-body")

    title = title_tag.get_text(strip=True) if title_tag else "No title found"
    body = body_tag.get_text(separator=" ", strip=True) if body_tag else "No content found"

    # Summarize if long enough
    summary = summarize_text(body, ratio=0.3) if len(body.split()) > 50 else body

    return {
        "url": url,
        "title": title,
        "summary": summary
    }

def get_articles():
    """Main function to get all articles from target date."""
    print(f"Starting to get NewZimbabwe articles for {TARGET_DATE}")
    links = get_filtered_posts()

    articles = []
    for link in links:
        article_data = get_article_data(link)
        articles.append(article_data)

    print(f"Done getting {len(articles)} articles from NewZimbabwe")
    return articles

# Example usage
if __name__ == "__main__":
    articles = get_articles()
    for i, art in enumerate(articles, 1):
        print(f"{i}. {art['title']} - {art['summary']}")
