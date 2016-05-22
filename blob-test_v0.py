from textblob import TextBlob
import newspaper

#keyword = input("Please enter the keyword: ")
keyword = "Apple" #for testing only
keyword_lowercase = keyword.lower()

search_string = "" # only for google news
split_keyword = keyword.split()
for i in range(len(split_keyword)):
    search_string += split_keyword[i]
    if i != len(split_keyword)-1:
        search_string += '+'

def google_news_site(search_query):
    prefix = 'http://news.google.com/news?q='
    return prefix+search_string

def cnn_news_site(search_query):
    prefix = 'http://cnn.com/search/?text='
    suffix = '&sections='
    return prefix+search_query+suffix

#Currently for news.google.com only
url_string = google_news_site(search_string)
my_url = "https://encrypted.google.com/#safe=active&hl=en&tbm=nws&q=apple+stock"
url_2 = "http://cnn.com"
cnn_url = cnn_news_site(search_string)

paper = newspaper.build(cnn_url, memoize_articles=False)

def sentiment(text):
    return TextBlob(text).sentiment.polarity

current_sum = 0.0
relevant_article_count = 0
for article in paper.articles:
    #article.download()
    #article.parse()
    print(article.url)
    article_text = article.text
    article_text_lowercase = article_text.lower()
    if keyword_lowercase in article_text_lowercase:
        current_sum += sentiment(article_text)

print("Article count is", str(relevant_article_count)+".")

rating = current_sum/max(relevant_article_count, 1)
print("The rating for", keyword, "is", str(rating)+".")
