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

    TL = LerTL(30)
    for post in TL:
        id = post.id_str
        user = post.user.id_str
        print(post)
        print(id)
        if user == MyID or '1164179019849502720' or '975853681831706624':
            continue
        else:
            Favorite(id)
            AddFriend(user)
            time.sleep(10)

    GetTrends()


    Unfollow()



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

def Unfollow():
    list = api.friends_ids()
    for friend in list:
        if friend == '1164179019849502720' or '975853681831706624':
            print(friend)
        else:
            api.destroy_friendship(friend)

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

def ShortURL(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

def MontaTxt(article,Tag):
    if (Tag == None):
        Tag = 'None'
    print(article)
    titulo, descricao, url, fonte, author = article['title'], article['description'], article['url'], article['source']['name'], article['author']
    url_short = ShortURL(url)


    if (Tag == 'None'):
        TD = len(titulo) + len(descricao) + len(url) + len(author)                   #22 são os caracteres fixos
        TDs = len(titulo) + len(descricao) + len(url)
        SPa = len(titulo) + len(descricao) + len(url_short) + len(author)

        # 280 - 22
        if (TD <= 258):
            return titulo + '.\n\n' + descricao + '\n\nAutor: ' + author + '\nVeja em: ' + url
        #280 - 14
        elif (TDs <= 266):
            return titulo + '.\n\n' + descricao + '\n\nVeja em: ' + url
        #280 - 22
        elif (SPa <= 258):
            return titulo + '.\n\n' + descricao + '\n\nAutor: ' + author + '\nVeja em: ' + url_short
        else:
            return titulo + '.\n\n' + descricao + '\nVeja em: ' + url_short

    else:
        TG = len(titulo) + len(descricao) + len(Tag) + len(url) + len(author)  # 22 são os caracteres fixos
        TGs = len(titulo) + len(descricao) + len(Tag) + len(url)
        SPa = len(titulo) + len(descricao) + len(Tag) + len(url_short) + len(author)
        # 280 - 24
        if (TG <= 256):
            return titulo + '.\n\n' + descricao + '\n\n' + Tag + '\n\nAutor: ' + author + '\nVeja em: ' + url
        # 280 - 15
        elif (TGs <= 265):
            return titulo + '.\n\n' + descricao + '\n\n' + Tag + '\nVeja em: ' + url
        # 280 - 24
        elif (SPa <= 256):
            return titulo + '.\n\n' + descricao + '\n\n' + Tag + '\n\nAutor: ' + author + '\nVeja em: ' + url_short
        # elif MontaTxt(article,Tag='None') < 280:
        #         return MontaTxt(article,Tag='None')
        else:
            return titulo + '.\n\n' + descricao + '\n\n' + Tag + '\nVeja em: ' + url_short


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
        Everything = newsapi.get_everything(language='pt', sort_by='popularity', q=query)
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
            print(trend)
            if (trend['tweet_volume'] > 10000 ):
                Everything = newsapi.get_everything(sort_by='relevancy', q=trend['name'])
                print(Everything)
                time.sleep(1)
                count = 0
                article = Everything['articles'][count]

                # if article['source']['name'] in 'Papelpop.com' or 'Publico.pt':
                #     article = Everything['articles'][++count]
                #     print("Papelpop ou pt" + article)

                Image = Download(article['urlToImage'])

                if '#' in str(trend['name']):
                    text = MontaTxt(article, Tag=trend['name'])
                    print('Com #: ' + text)
                else:
                    text = MontaTxt(article, Tag='None')
                    print('Sem #: ' + text)

                if (Image != "None"):
                    f = open("tweets.txt", "r")
                    r = f.read()
                    if not article['title'] in r:
                        Tweet(text)
                        #api.update_with_media(Image, text)
                        f.close()
                        f = open("tweets.txt", "a")
                        f.write(article['title'])
                        f.close()
                    else:
                        pass
                else:
                    f = open("tweets.txt", "r")
                    r = f.read()
                    if not article['title'] in r:
                        Tweet(text)
                        f.close()
                    else:
                        pass

                print('Twettou!')
                time.sleep(1800)
                os.remove('C:\\Users\\joaop\\PycharmProjects\\Twitter Bot\\Images\\' + Image)

        except:
            pass
        time.sleep(8)


if __name__ == '__main__':
    main()