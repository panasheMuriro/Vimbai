import requests
from bs4 import BeautifulSoup
from .summarize import summarize_text  # import reusable function

from utils.get_yesterday_date import get_yesterday_date

previous_date = get_yesterday_date('news_dze_zimbabwe')

BASE_URL = 'https://www.newsdzezimbabwe.co.uk/'
TARGET_DATE = previous_date
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def get_filtered_posts():
    """Fetch entries on the target date."""
    resp = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    entries = soup.find_all(class_='hentry')

    filtered = []
    for entry in entries:
        date_tag = entry.find(class_='meta_date')
        if date_tag and date_tag.get_text(strip=True) == TARGET_DATE:
            a_tag = entry.select_one('.entry-title a')
            if a_tag and a_tag.get('href'):
                url = a_tag['href']
                if not url.startswith('http'):
                    url = BASE_URL.rstrip('/') + '/' + url.lstrip('/')
                filtered.append(url)
    return list(set(filtered))  # deduplicate

def get_article_data(url):
    """Fetch heading and summary for an article URL."""
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')

    heading_tag = soup.select_one('.hentry .entry-title a')
    if heading_tag:
        heading = heading_tag.get_text(strip=True)
    else:
        heading_tag = soup.select_one('.hentry .entry-title')
        heading = heading_tag.get_text(strip=True) if heading_tag else "No heading found"

    content_tag = soup.select_one('.hentry .entry-content')
    content = content_tag.get_text(separator=' ', strip=True) if content_tag else "No content found"

    summary = summarize_text(content, ratio=0.3) if len(content.split()) > 50 else content

    return {
        "url": url,
        "title": heading,
        "summary": summary
    }

def get_articles():
    """Main function to get all articles for the target date."""
    print(f"Starting to get NewsDzeZimbabwe articles for {TARGET_DATE}")
    links = get_filtered_posts()

    articles = []
    for link in links:
        article_data = get_article_data(link)
        articles.append(article_data)

    print(f"Done getting {len(articles)} articles from NewsDzeZimbabwe")
    return articles

# Example usage
if __name__ == "__main__":
    articles = get_articles()
    for i, art in enumerate(articles, 1):
        print(f"{i}. {art['heading']} - {art['summary']}\n")
