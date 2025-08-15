# run_scrapers.py
from scrappers.zimeye import get_articles as get_articles_zimeye
from scrappers.pindula import get_articles as get_articles_pindula
from scrappers.new_zimbabwe import get_articles as get_articles_newzimbabwe
from scrappers.news_day import get_articles as get_articles_newsday
from scrappers.news_dze_zimbabwe import get_articles as get_articles_newsdze

def run_all_scrapers():
    """Run all scrapers and combine articles into one list."""
    all_articles = []

    print("Fetching ZimEye articles...")
    zimeye_articles = get_articles_zimeye()
    all_articles.extend(zimeye_articles)

    print("Fetching Pindula articles...")
    pindula_articles = get_articles_pindula()
    all_articles.extend(pindula_articles)

    print("Fetching NewZimbabwe articles...")
    newzimbabwe_articles = get_articles_newzimbabwe()
    all_articles.extend(newzimbabwe_articles)

    print("Fetching NewsDay articles...")
    newsday_articles = get_articles_newsday()
    all_articles.extend(newsday_articles)

    print("Fetching NewsDzeZimbabwe articles...")
    newsdze_articles = get_articles_newsdze()
    all_articles.extend(newsdze_articles)

    return all_articles

if __name__ == "__main__":
    articles = run_all_scrapers()
    for i, art in enumerate(articles, 1):
        title_or_heading = art.get("title") or art.get("heading") or "No title"
        author = art.get("author", "")
        summary = art.get("summary", "")
        print(f"{i}. {title_or_heading} {f'by {author}' if author else ''} - {summary}\n")
