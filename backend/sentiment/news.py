import os
from eventregistry import EventRegistry,QueryArticlesIter
def getNewsOnTopic(country,category):
    er = EventRegistry(apiKey = os.getenv("NEWS_API_KEY"))
    query = {
    "$query": {
        "$and": [
        {
            "conceptUri": "http://en.wikipedia.org/wiki/"+category
        },
        {
            "locationUri": "http://en.wikipedia.org/wiki/"+ country
        }
        ]
    },
    "$filter": {
        "forceMaxDataTimeWindow": "31"
    }
    }
    q = QueryArticlesIter.initWithComplexQuery(query)
    return q.execQuery(er, maxItems=100)
def setupSentiment(category,countries,red):
    for country in countries:
        avg=0
        nr=0
        for article in getNewsOnTopic(country,category):
            if article["sentiment"]!=None:
                nr+=1
                avg+=article["sentiment"]
        if nr!=0:
            avg/=nr
            red.set(country,avg)
        else:
            red.set(country,0)

    
    