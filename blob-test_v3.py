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
# * Nested everything in a big function
# * Function accepts keyword and day.
# * day is a datetime object
# * Only process at most one page (simpler and saves time)

#######################
# ISSUES
#---------------
# * Within-24-hour check only accurate to 2 days, cuz timezone is ass
# * Date is none at times (possibly with special unicode characters)

########################
# FUTURE
# ----------------------
# * Speed crawling up
# * If it is sped up, include more than one page search but still have a cap

def go(keyword, query_date): # day is a datetime object
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

    ''' mention language locale setting '''
    locale_language = getdefaultlocale()[0][:2] # not sure if always works

    keyword_lowercase = keyword.lower()

    URL = "https://www.google.ca/search?q={query}&safe=strict&hl=en&as_drrb=b&authuser=0&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{start}%2Ccd_max%3A{end}&tbm=nws"

    search_string = "" # only for google news
    split_keyword = keyword.split()
    for i in range(len(split_keyword)):
        search_string += split_keyword[i]
        if i != len(split_keyword)-1:
            search_string += '+'

    string_query_date = query_date.isoformat()
    html_page = run(query=search_string, start = string_query_date, end = string_query_date)
    html_page = str(html_page)
    url_indices = start_substrings(html_page)

    for start, end in url_indices:
        i = start
        while html_page[i] != '&':
            i += 1
        PREFIX_LENGTH = 16
        print(html_page[start+PREFIX_LENGTH:i])
        if "http://www.forbes.com" in html_page[start+PREFIX_LENGTH:i]:
            print("SKIPPING FORBES CUZ IT'S SHIT")
            print("-------------------------------")
            continue
        article = newspaper.Article(url=html_page[start+PREFIX_LENGTH:i], language=locale_language)
        article.download()
        date = None
        try:
            article.parse()
            date = str(article.publish_date)
        except:
            print("ERROR: DOWNLOAD FAILED")
            print("----------------------------------")
            continue
        if date == 'None':
            print("FAILURE: UNSUCESSFUL DOWNLOAD. PROOF: date=", date)
            print("----------------------------------")
            continue
        else:
            print("date is", date)
            print("SUCESSFUL")
            print("date", date, date.split()[0])
            dtobj=datetime.datetime.strptime(date.split()[0], "%Y-%m-%d")
            print("dtobj", dtobj)
            time = date.split()[1]
            print("time", time)
            if "-" not in time and "+" not in time:
                tzhour = 0
                tzmin = 0
                print(tzhour, tzmin)
            else:
                tzhour, tzmin = time.split("-")[0].split("+")[-1].split(":")
                tzhour, tzmin = -int(tzhour), -int(tzmin) #if -4:00, add 4 to get UTC
                print(tzhour, tzmin)
            article_delta = datetime.timedelta(hours=tzhour, minutes = max(1, tzhour/max(abs(tzhour), 1))*abs(tzmin))
            print(article_delta)
            local_delta = datetime.datetime.utcnow()-datetime.datetime.now()

            if query_date+local_delta-dtobj-article_delta > datetime.timedelta(days=1):
                print("TOO OLD: published", dtobj, "query", query_date)
                print("----------------------------------")
                continue
        print("WE'RE DOING IT BOYS")

        full_text = str(article.text) # not sure if str() is needed
        current_sum += sentiment(full_text)

        print("sentiment is", sentiment(full_text))
        print("publish date is", date)
        print("----------------------------------")

        relevant_article_count += 1




    print("Article count is", str(relevant_article_count)+".")

    rating = current_sum/max(relevant_article_count, 1)
    print("The total rating is", str(current_sum)+".")
    print("The rating for", keyword, "is", str(rating)+".")

'''TEST'''
day = datetime.datetime.strptime("2016-05-21", "%Y-%m-%d")
go("Apple", day)
