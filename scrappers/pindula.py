import requests
from bs4 import BeautifulSoup
from .summarize import summarize_text  # import reusable function
from utils.get_yesterday_date import get_yesterday_date

previous_date = get_yesterday_date('pindula')
BASE_URL = 'https://news.pindula.co.zw/'
TARGET_DATE_PATH = previous_date
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def get_articles():
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.select('.wp-block-post a')
    unique_links = set(href.get('href', '') for href in links if TARGET_DATE_PATH in href.get('href', ''))

    articles = []
    print("Starting to get Pindula articles for ", previous_date)
    for link in unique_links:
        article_resp = requests.get(link, headers=HEADERS)
        article_soup = BeautifulSoup(article_resp.text, 'html.parser')

        author_tag = article_soup.select_one('.wp-block-post-author-name')
        author = author_tag.get_text(strip=True) if author_tag else "No author found"

        header_tag = article_soup.select_one('.wp-block-post-title')
        header = header_tag.get_text(strip=True) if header_tag else "No header found"

        content_tag = article_soup.select_one('.entry-content')
        content = content_tag.get_text(separator=' ', strip=True) if content_tag else "No content found"

        # Use reusable summarize function
        summary = summarize_text(content, ratio=0.3) if len(content.split()) > 50 else content

        articles.append({
            'url': link,
            'title': header,
            'author': author,
            # 'content': content,
            'summary': summary
        })
    
    print(f"Done getting {len(articles)} articles from Pindula")
    return articles

# Example usage
if __name__ == "__main__":
    articles = get_articles()
    for i, art in enumerate(articles, 1):
        print(f"{i}. {art['header']} - {art['summary']}")
