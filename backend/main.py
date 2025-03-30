import asyncio
import redisSetup
import sentiment.news
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
r=redisSetup.setup()
print(sentiment.news.getNewsOnTopic("alegeri",(datetime.now()-timedelta(days=1)).date(),datetime.now().date()))


