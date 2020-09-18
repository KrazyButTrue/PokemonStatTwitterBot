import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener 
import json
import re
import requests 

consumer_key = 'bAWoCmgdbMZHoi8TdRVFm27kd'
consumer_secret = 'FzbSEKsCIdBzhmmzuxnOL8t10JXOIKmcRImBmi0ZClA2wa4NRA'

key = '1268799124780040192-B7wNjLWNTXT7ir6fYYBxh6HNV6EUWx'
secret = '4tfxCbFoOgycO7VY7SmJVo1wyZDC7w2jw3Re3eFYmksjh'

class StdOutListener(StreamListener):
    def on_data(self, data):
        real_data = json.loads(data)
        id = real_data["id"]
        tweet = real_data['text']
        author = real_data['user']['screen_name']
        replyToTweet(tweet, id, author)

    def on_error(self, status):
        print(status)

def replyToTweet(tweet, id, author):
    #Step 1: Decode Tweet
    pokename = scanning(tweet)
    #Step 2: Call  API for information
    r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokename}')
    pokeinfo = r.json()
    poke_stats = pokeinfo["stats"]
    poketype = pokeinfo["types"][0]["type"]["name"]
    stat_names = []
    base_stats = []
    for stat in poke_stats:
        stat_names.append(stat["stat"]["name"])
        base_stats.append(stat["base_stat"])
    statistics = dict(zip(stat_names, base_stats))
    #Step 3: Tweet back information
    new_tweet = f"Hello {author}, here are {pokename}'s stats: \nType: {poketype} \n"
    for key, value in statistics.items():
        new_tweet += f"{key} : {value} \n"
    #Step 4: Reply to Tweet
    reply(new_tweet, id)

def scanning(tweet):
    pokemon = re.findall(r'[\"“”](.+?)[\"“”]',tweet)
    pokemon_name = pokemon[0].lower()
    return pokemon_name

def authentication():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)
    return api, auth

def startStreaming():
    api, auth = authentication()
    listener = StdOutListener()
    stream = Stream(auth, listener)
    stream.filter(track=["@WillieTwitBot"])

def reply(tweet, id):
    api, auth = authentication()
    api.update_status(tweet, in_reply_to_status_id=id, auto_populate_reply_metadata=True)

if __name__ == "__main__":
    startStreaming()

