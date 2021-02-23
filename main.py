import sys
import wget
import time
import tweepy
import geocoder
import pyshorteners
import os

from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='039d4d477bd047c989b07582dd19b422')
API_KEY = 'o_1ese91vvm3'
MyID = '1155543639428349953'

auth = tweepy.OAuthHandler('yoLKzvVI3qeRCw1M5mbL51xxH', 'YNgzukhTtnCaaRtBgAGqBEYMJeJZd3rm7EqKofCb8KszysxVOt')
auth.set_access_token('1155543639428349953-maeGPwFJFxKjjphICQxZIFwCVraX7W', 'VFUMMjID72TotGxzE0np3zpzB0ouhaHiHVqq07oxD1DEW')

api = tweepy.API(auth)

def main():
    # Mentions = GetMentions(100)
    # for mention in Mentions:
    #     id = mention.id
    #     user = mention.user.id
    #     Favorite(id)
    #     AddFriend(user)

    GetTrends()

    # TL = LerTL(100)
    # for post in TL:
    #     id = post.id
    #     user = post.user.id
    #     if str(user) != MyID:
    #         Favorite(id)
    #         AddFriend(user)

    #Everything()



def Search(assunto, quantidade):
    for tweet in tweepy.Cursor(api.search, q=assunto).items(quantidade):
        return tweet

def AddFriend(id):
    try:
        api.create_friendship(id)
    except:
        pass

def Favorite(id):
    try:
        api.create_favorite(id)
    except:
        pass

def LerTL(quantidade):
    public_tweets = api.home_timeline(quantidade)
    return public_tweets

def GetMentions(quantidade):
    return api.mentions_timeline(quantidade)

def GetUser(id):
    user = api.get_user(id)
    print(user.screen_name)
    print(user.followers_count)
    for friend in user.friends():
        print(friend.screen_name)

def Tweet(txt):
    api.update_status(txt)

def Retweet(id):
    return api.retweet(id)

def GetFollowersID():
    for follower in tweepy.Cursor(api.followers).items():
        print(follower.id)
        return follower.id

def GetStatus(id):
    status = api.get_status(id, tweet_mode="extended")
    return status

def Download(url):
    try:
        filename = wget.download(url, r'C:\Users\joaop\PycharmProjects\Twitter Bot\Images')
        return filename
    except:
        return 'None'
        pass

def ShortURL(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

def MontaTxt(article,Tag):
    if (Tag == None):
        Tag = 'None'
    print(article['title'])
    print(Tag)
    titulo, descricao, url, fonte = article['title'], article['description'], article['url'], article['source']['name']
    url = ShortURL(url)
    if (fonte == 'None'):
        fonte = ''

    if (Tag == 'None'):
        TS = len(descricao) + len(titulo) + len(url) + 9
        if(TS <= 262):
            return titulo + '\n' + descricao + '\n\nFonte: ' + fonte + '\nVeja em: ' + url
        else:
            return titulo + '\n\nFonte: ' + fonte + '\nVeja em: ' + url
    else:
        TS = len(descricao) + len(titulo) + len(url) + 9 + len(Tag)
        if (TS <= (260 - len(Tag))):
            return titulo + '\n' + descricao + '\n' + '#' + Tag + '\n\nFonte: ' + fonte + '\nVeja em: ' + url

def Top():
    try:
        top_headlines = newsapi.get_top_headlines(country='br')
        for article in top_headlines['articles']:
            text = MontaTxt(article)
            if (article['urlToImage'] != "null"):
                Image = Download(article['urlToImage'])
                api.update_with_media(Image, text)
                print('Twettou!')
                time.sleep(100)
    except:
        print("oi")

def Everything(query):
    try:
        Everything = newsapi.get_everything(language='pt', sort_by='relevancy', q=query)
        for article in Everything['articles']:
            text = MontaTxt(article)
            Image = Download(article['urlToImage'])
            if (Image != "None"):
                api.update_with_media(Image, text)
            else:
                Tweet(text)
            print('Twettou!')
            time.sleep(100)
    except:
        print('oi')

def GetTrends():
    loc = 'Brasil'
    g = geocoder.osm(loc)
    closest_loc = api.trends_closest(g.lat, g.lng)
    Trends = api.trends_place(closest_loc[0]['woeid'])
    trends = Trends[0]['trends']

    for trend in trends:
        try:
            if (trend['tweet_volume'] > 1 ):
                Everything = newsapi.get_everything(language='pt', sort_by='relevancy', q=trend['name'])
                print(Everything)
                print(Everything['articles'])
                article = Everything['articles'][0]
                print('Passou')
                Image = Download(article['urlToImage'])

                if '#' in str(trend['name']):
                    text = MontaTxt(article, trend['name'])
                    print('Com trend: ' + text)
                else:
                    text = MontaTxt(article, Tag='None')
                    print('Sem trend: ' + text)

                if (Image != "None"):
                    api.update_with_media(Image, text)
                #else:
                   #Tweet(text)

                print('Twettou!')
                #os.remove(r'Images/'+Image)
            else:
                print("nao")
        except:
            pass


if __name__ == '__main__':
    main()