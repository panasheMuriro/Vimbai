import requests
from bs4 import BeautifulSoup

url = 'https://www.newsday.co.zw/category/16/local-news'
target_date = "Aug. 11, 2025"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

boda_elements = soup.select('.boda-bottom')

filtered_elements = []

for elem in boda_elements:
    if elem.select_one('.premium, .Premium'):
        continue

    date_tag = elem.select_one('.display-style')
    if date_tag and date_tag.get_text(strip=True) == target_date:
        filtered_elements.append(elem)

print(f"Found {len(filtered_elements)} entries with date {target_date} excluding ones containing .premium\n")

for i, elem in enumerate(filtered_elements, 1):
    print(f"Entry {i}:")

    first_link = elem.find('a')
    if not first_link or not first_link.get('href'):
        print("No link found")
        print('-' * 40)
        continue

    article_url = first_link['href']
    print(f"Visiting link: {article_url}")

    article_resp = requests.get(article_url, headers=headers)
    article_soup = BeautifulSoup(article_resp.text, 'html.parser')

    # Get title from <h1>
    title_tag = article_soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    # Get content from .content-body
    content_tag = article_soup.select_one('.content-body')
    content = content_tag.get_text(separator=' ', strip=True) if content_tag else "No content found"

    # Get author from <small class="text-muted">
    author_tag = article_soup.select_one('small.text-muted')
    author = author_tag.get_text(strip=True) if author_tag else "No author found"

    print(f"Title: {title}")
    print(f"Author: {author}")
    print(f"Content snippet: {content[:500]}...\n{'-'*60}\n")
