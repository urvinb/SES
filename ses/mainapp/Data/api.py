import pprint 
import requests
import pandas as pd
import json


secret = 'cc9d9e15c4ca4e99ba40370b2bea4eee'

def india_headlines():
    url = 'https://newsapi.org/v2/top-headlines'

    parameters = { 
        'country':'in',
        'q': 'gre',
        'apiKey': secret # your own API key 
    } 
    
    # Make the request 
    response = requests.get(url, params = parameters) 
    
    x = response.json()
    df = pd.DataFrame(x['articles'])
    return df

def world_headlines():
    url = 'https://newsapi.org/v2/everything'

    parameters = { 
        'q': 'exam',
        'apiKey': secret # your own API key 
    } 
    
    # Make the request 
    response = requests.get(url, params = parameters) 
    print(response.content)
    
    x = response.json()
    df = pd.DataFrame(x['articles'])
    return df




