# Why use twint?

Twint allows to scrape way more than ~3200 tweets for given user! It does fail sometimes while querying the data, so it makes sense to retry, but only for period we still haven't received data. We store it as json because that makes it easy to parse tweet texts and choose other relevant fields. Finally we store it as csv files to be used in our analysis.
