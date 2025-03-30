import os
import sys
sys.path.append('../backend') 
import redisSetup
from eventregistry import EventRegistry,QueryArticlesIter
def getNewsOnTopic(country,category):
    er = EventRegistry(apiKey = os.getenv("NEWS_API_KEY"))
    query = {
    "$query": {
        "$and": [
        {
            "categoryUri": "dmoz/Society/"+category
        },
        {
            "locationUri": "http://en.wikipedia.org/wiki/"+country
        }
        ]
    },
    "$filter": {
        "forceMaxDataTimeWindow": "31",
        "startSourceRankPercentile": 0,
        "endSourceRankPercentile": 50,
        "isDuplicate": "skipDuplicates"
    }
    }
    q = QueryArticlesIter.initWithComplexQuery(query)
    return q.execQuery(er, maxItems=100)
def setupSentiment(category,countries,red):
    v_max=0
    v_min=0
    sentiments={}
    for country in list(set(countries)):
        country=country.replace(' ','_')
        sentiments.setdefault(country,{})
        size={}
        for article in getNewsOnTopic(country,category):
            if article['sentiment']!=None:
                v_max=max(v_max,article['sentiment'])
                v_min=min(v_min,article['sentiment'])
                sentiments[country].setdefault(article['date'], 0)
                sentiments[country][article['date']] += article['sentiment']
                size.setdefault(article['date'],0)
                size[article['date']]+=1
        if len(sentiments[country]) > 0:
            for date in sentiments[country].keys():
                sentiments[country][date]/=size[date]
    for country in sentiments.keys():
        for date in sentiments[country].keys():
            sentiments[country][date]-=v_min
            sentiments[country][date]/=(v_max-v_min)
        if len(sentiments[country]) > 0:
            red.hset(country,mapping=sentiments[country])
# setupSentiment("Crime",["dkasj"],redisSetup.redisSetup())