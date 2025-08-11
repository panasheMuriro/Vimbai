from newspaper import Article

url = 'https://www.newsdzezimbabwe.co.uk/'
article = Article(url)
article.download()
article.parse()

print(article.title,  article.publish_date)
