# StockSentiment

# Guidelines

* You should use `sudo` to run all Python `newspaper` `download()` commands.

# Included software

1. TextBlob
2. Newspaper3k

First `cd /path/to/file`.

## Install TextBlob
    $ sudo pip3 install -U textblob
    $ python3 -m textblob.download_corpora

## Install Newspaper3k
    $ sudo apt-get install python-dev
    $ sudo apt-get install libxml2-dev libxslt-dev #3?
	$ sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev
	$ sudo pip3 install newspaper3k
	$ curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3
