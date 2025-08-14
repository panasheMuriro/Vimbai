import requests
from bs4 import BeautifulSoup
from .summarize import summarize_text  # Import reusable function

BASE_URL = 'https://www.newsday.co.zw/category/16/local-news'
TARGET_DATE = "Aug. 13, 2025"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def get_filtered_posts():
    """Fetches links to articles on the target date, excluding premium ones."""
    resp = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')

    boda_elements = soup.select('.boda-bottom')
    filtered_links = set()

    for elem in boda_elements:
        if elem.select_one('.premium, .Premium'):
            continue

        date_tag = elem.select_one('.display-style')
        if date_tag and date_tag.get_text(strip=True) == TARGET_DATE:
            first_link = elem.find('a', href=True)
            if first_link:
                filtered_links.add(first_link['href'])

    return list(filtered_links)

def get_article_data(url):
    """Fetches title, author, and summary from an article URL."""
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')

    title_tag = soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    content_tag = soup.select_one('.content-body')
    content = content_tag.get_text(separator=' ', strip=True) if content_tag else "No content found"

    author_tag = soup.select_one('small.text-muted')
    author = author_tag.get_text(strip=True) if author_tag else "No author found"

    summary = summarize_text(content, ratio=0.3) if len(content.split()) > 50 else content

    return {
        "url": url,
        "title": title,
        "author": author,
        "summary": summary
    }

def get_articles():
    """Main function to get all articles for the target date."""
    print(f"Starting to get NewsDay articles for {TARGET_DATE}")
    links = get_filtered_posts()

    articles = []
    for link in links:
        article_data = get_article_data(link)
        articles.append(article_data)

    print(f"Done getting {len(articles)} articles from NewsDay")
    return articles

# Example usage
if __name__ == "__main__":
    articles = get_articles()
    for i, art in enumerate(articles, 1):
        print(f"{i}. {art['title']} by {art['author']} - {art['summary']}\n")
