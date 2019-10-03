
import urllib.request,json
from .models import Quotes
from . import request
from config import Config



# Getting the movie base url
base_url = None

def configure_request(app):
    global base_url

    base_url = Config.QUOTES_API





def getQuotes():
   random_quote = request.get(base_url)
   new_quote = random_quote.json()
   id = new_quote.get("id")
   author = new_quote.get("author")
   permalink = new_quote.get("permalink")
   quote = new_quote.get("quote")
   quote_object = Quotes(id,author,quote,permalink)
   return quote_object