import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.newzimbabwe.com/category/news/"
TARGET_DATE = "11th August 2025"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def get_filtered_posts():
    resp = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    posts = soup.select(".post-grid-content")

    filtered = []
    for post in posts:
        footer = post.select_one(".post-grid-content-footer")
        if footer and TARGET_DATE in footer.get_text(strip=True):
            link_tag = post.find("a", href=True)
            if link_tag:
                filtered.append(link_tag["href"])
    return list(set(filtered))  # Remove duplicates

def get_article_data(url):
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.select_one(".post-title")
    body_tag = soup.select_one(".post-body")

    title = title_tag.get_text(strip=True) if title_tag else None
    body = body_tag.get_text(separator="\n", strip=True) if body_tag else None

    return {
        "url": url,
        "title": title,
        "body": body
    }

if __name__ == "__main__":
    links = get_filtered_posts()
    print(f"Found {len(links)} posts from {TARGET_DATE}\n")

    for link in links:
        article = get_article_data(link)
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Body: {article['body'][:300]}...")  # Preview first 300 chars
        print("-" * 80)
