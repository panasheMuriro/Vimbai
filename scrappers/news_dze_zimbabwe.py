import requests
from bs4 import BeautifulSoup

base_url = 'https://www.newsdzezimbabwe.co.uk/'
target_date = "Monday, August 11, 2025"
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')
filtered_entries = []

entries = soup.find_all(class_='hentry')

for entry in entries:
    date_tag = entry.find(class_='meta_date')
    if date_tag and date_tag.get_text(strip=True) == target_date:
        filtered_entries.append(entry)

for i, entry in enumerate(filtered_entries, 1):
    a_tag = entry.select_one('.entry-title a')
    if not a_tag or 'href' not in a_tag.attrs:
        print(f"Entry {i} has no valid link, skipping...")
        continue

    article_url = a_tag['href']
    if not article_url.startswith('http'):
        article_url = base_url.rstrip('/') + '/' + article_url.lstrip('/')

    article_resp = requests.get(article_url)
    article_soup = BeautifulSoup(article_resp.text, 'html.parser')

    # Extract heading text from article page
    heading_tag = article_soup.select_one('.hentry .entry-title a')
    if heading_tag:
        heading = heading_tag.get_text(strip=True)
    else:
        # fallback: just .entry-title text if no <a> inside
        heading_tag = article_soup.select_one('.hentry .entry-title')
        heading = heading_tag.get_text(strip=True) if heading_tag else "No heading found"

    # Extract content text
    content_tag = article_soup.select_one('.hentry .entry-content')
    content = content_tag.get_text(separator=' ', strip=True) if content_tag else "No content found"

    print(f"Article {i}:")
    print(f"URL: {article_url}")
    print(f"Heading: {heading}")
    print(f"Content:\n{content}\n{'-'*40}\n")
