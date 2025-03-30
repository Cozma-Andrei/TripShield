import os
import requests

def getNewsOnTopic(topic, startDate, endDate):
    apiKey=os.getenv("NEWS_API_KEY")
    url="https://newsapi.org/v2/everything"
    response=requests.get(url,params={
        "q":topic,
        "from":startDate,
        "to":endDate
    },headers={
        "X-Api-Key": apiKey
    })
    return response.json()
