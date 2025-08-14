# run the scrappers to get the content

from scrappers.zimeye import get_articles

from scrappers.pindula import get_articles as get_articles_pindula
zimeye_articles = get_articles()

pindula_articles = get_articles_pindula()
print(pindula_articles)
# print(articles)