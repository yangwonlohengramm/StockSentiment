from textblob import TextBlob
import requests
import time
import re
import newspaper
from locale import getdefaultlocale

#######################
# ISSUES
#---------------
# * Date is not accurate, cuz URL is fucked
# * Search source was Gulf News (fuck gulf news)
# * Only does one page

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

URL = 'https://www.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&as_q={query}&as_occt=any&as_drrb=b&as_mindate={month}%2F%{from_day}%2F{year}&as_maxdate={month}%2F{to_day}%2F{year}&authuser=0'

search_string = "" # only for google news
split_keyword = keyword.split()
for i in range(len(split_keyword)):
    search_string += split_keyword[i]
    if i != len(split_keyword)-1:
        search_string += '+'


#DATE NOT WORKING
html_page = run(query=search_string, month=cur_month, from_day=cur_day-1, to_day=cur_day, year=cur_year)
# for some reason doesn't change if I change cur_month to cur_month-1 etc.
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
        if article.publish_date == None:
            print("no date")
            print(article.publish_date)
            print("----------------------------------")
            continue
        full_text = str(article.text) # not sure if str() is needed
        current_sum += sentiment(full_text)

        print("sentiment is", sentiment(full_text))
        print("publish date is", article.publish_date)
        print("----------------------------------")

        relevant_article_count += 1
    except: # some websites are weird like http://seekingalpha.com/article/3976559-apple-gives-car-money-china-r-and-d-india
        continue




print("Article count is", str(relevant_article_count)+".")

rating = current_sum/max(relevant_article_count, 1)
print("The total rating is", str(current_sum)+".")
print("The rating for", keyword, "is", str(rating)+".")
