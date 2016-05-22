from textblob import TextBlob
import requests
import time
import re
import newspaper
import datetime
from locale import getdefaultlocale

#######################
# UPDATES
# ---------------------
# * Date now is accurate within 2 days += 1 day
# * Fixed gulf news shit

#######################
# ISSUES
#---------------
# * Date is not accurate, cuz URL is -f-u-c-k-e-d- sketchy
# * Only does one page
# * Within-24-hour check only accurate to 2 days, cuz timezone is ass

def run(**params):
    print(URL.format(**params))
    response = requests.get(URL.format(**params))
    #print(response.content, response.status_code)
    return response.content

'''mention kmp/while, .find/regex thing'''
def start_substrings(string):
    l = []
    for m in re.finditer('<a href=', string):
        start = int(m.start())
        end = int(m.end())
        if string[end+1:end+8]== "/url?q=":
            l.append((int(m.start()), int(m.end())))
    return l

def sentiment(text):
    return TextBlob(text).sentiment.polarity

current_sum = 0.0
relevant_article_count = 0

cur_day = int(time.strftime("%d"))
cur_month = int(time.strftime("%m"))
cur_year = int(time.strftime("%Y"))
''' mention language locale setting '''
locale_language = getdefaultlocale()[0][:2] # not sure if always works
print(cur_day, cur_month, cur_year)

keyword = input("Please enter the keyword: ")
#keyword = "Apple" #for testing only
keyword_lowercase = keyword.lower()

URL = "https://www.google.ca/search?hl=en&tbm=nws&as_q={query}&as_occt=any&as_drrb=b&authuser=0&gws_rd=cr&ei=eRhBV9-sGMnOyALkwYr4Cw&start={page_number}#q={query}&safe=active&hl=en&authuser=0&tbm=nws&tbs=qdr:d"

search_string = "" # only for google news
split_keyword = keyword.split()
for i in range(len(split_keyword)):
    search_string += split_keyword[i]
    if i != len(split_keyword)-1:
        search_string += '+'


html_page = run(query=search_string, page_number = (1-1)*10)
html_page = str(html_page)
url_indices = start_substrings(html_page)
print(url_indices)
for start, end in url_indices:
    i = start
    while html_page[i] != '&':
        i += 1
    PREFIX_LENGTH = 16
    print(html_page[start+PREFIX_LENGTH:i])
    article = newspaper.Article(url=html_page[start+PREFIX_LENGTH:i], language=locale_language)
    article.download()
    try:
        article.parse()
        date = str(article.publish_date)
        if date == None:
            print("no date")
            print(date)
            print("----------------------------------")
            continue
        else:
            dtobj=datetime.datetime.strptime(date.split()[0], "%Y-%m-%d")
            now = datetime.datetime.now()
            if now-dtobj > datetime.timedelta(days=2):
                print("more than two days timezone ignored ago")
                print("published", datetime.time(date), "today is", datetime.date.today())
                print("----------------------------------")
                continue

        full_text = str(article.text) # not sure if str() is needed
        current_sum += sentiment(full_text)

        print("sentiment is", sentiment(full_text))
        print("publish date is", date)
        print("----------------------------------")

        relevant_article_count += 1
    except:
        print("----------------------------------")
        continue




print("Article count is", str(relevant_article_count)+".")

rating = current_sum/max(relevant_article_count, 1)
print("The total rating is", str(current_sum)+".")
print("The rating for", keyword, "is", str(rating)+".")
