from twython import TwythonStreamer
from string import punctuation
import keys
import sqlite3
import sys


class MyStreamer(TwythonStreamer):
    """
    Setting up the streamer. Defining how to handle the signals that Twython
    Streamer API uses.
    """
    def on_success(self, data):

        # Just to have the count of how many tweets we are storing in the db
        # while harversting
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM TWEETS;")
        result = cursor.fetchone()
        successful_tweets = result[0]

        # We only take tweets that are in English
        if data['lang'] == 'en':
            # Inserting into Tweets Table
            self.insert_Tweet(data)

            # Inserting into Users Table
            self.insert_User(data, cursor)

            # Inserting into Produces Table
            self.insert_Productions(data)

            # Inserting into Mentions Table
            self.insert_Mentions(data)

            # Inserting into Hashtags Table
            self.insert_Hashtags(data)

            try:
                # Inserting into URLs Table
                self.insert_URLs(data)
            except:
                # Sometimes strange symbols appear
                pass

            # Inserting appropiate words into Words Table
            self.insert_Words(data)

            # Updating the original tweet if it is a retweet
            self.update_Retweet(data)

            # Inserting the timing of the tweet
            self.insert_Time(data)

            # We commit when everything has gone OK. If there is some kind
            # of error with the insertion the whole tweet insertion is
            # rolled back.
            conn.commit()

            # We show the count
            successful_tweets += 1
            print "%i tweets inserted succesfully." % successful_tweets

            if verbose:
                print data['user']['screen_name']
                print data['text']

    def on_error(self, status_code, data):
        print status_code

        # Wanting to insist to get the data even having an error?
        # Comment the next line!
        self.disconnect()

    def on_timeout():
        print '*** ERROR ***: The request has timed out.'

    def text_format(self, text):
        text = text.replace("&amp;", "&")
        text = text.replace("&gt;", ">")
        text = text.replace("&lt;", "<")
        text = text.replace("\'",  "\'\'")
        return text

    def insert_Tweet(self, data):
        # Inserting into Tweets Table depending on whether the coordinates
        # exist or not
        if data['coordinates'] is None:
            conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS, "
                         "FOLLOWERS) VALUES (%i, '%s', %i, %i, %i);"
                         % (data['id'], self.text_format(data['text']),
                            data['favorite_count'], data['retweet_count'],
                            data['user']['followers_count']))

        else:
            if data['coordinates']['type'] == 'Point':
                conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                             ", LAT, LONG, FOLLOWERS) "
                             "VALUES(%i, '%s',%i, %i,%f, %f, %i);"
                             % (data['id'], self.text_format(data['text']),
                                data['favorite_count'],
                                data['retweet_count'],
                                data['coordinates']['coordinates'][1],
                                data['coordinates']['coordinates'][0],
                                data['user']['followers_count']))

    def insert_User(self, data, cursor):
        # As SQLite3 don't have a boolean defined type we have to use ints
        if data['user']['verified'] == "True":
            verified = 1
        else:
            verified = 0

        # We have to see whether the user has already been stored or not
        cursor.execute("SELECT COUNT(*) FROM USERS WHERE ID=%s;"
                       % data['user']['id'])
        result = cursor.fetchone()
        if result[0] == 0:
            conn.execute("INSERT INTO USERS(ID, NAME, SCREEN_NAME, "
                         "VERIFIED, LANG) VALUES (%i, '%s', '%s', %i, "
                         "'%s');"
                         % (data['user']['id'],
                            self.text_format(data['user']['name']),
                            self.text_format(data['user']['screen_name']),
                            verified, data['user']['lang']))

    def insert_Productions(self, data):
        conn.execute("INSERT INTO PRODUCES(ID_TWEET, ID_USER) "
                     "VALUES (%i, %i);" % (data['id'], data['user']['id']))

    def insert_Mentions(self, data):
        # We avoid repeated mentions
        mentions = []
        [mentions.append(mention['id'])
         for mention in data['entities']['user_mentions']
         if mention['id'] not in mentions]

        for user in mentions:
            conn.execute("INSERT INTO MENTIONS (ID_TWEET, ID_USER) "
                         "VALUES (%i, %i);" % (data['id'], user))

    def insert_Hashtags(self, data):
        # We avoid repeated hashtags
        hashtags = []
        [hashtags.append(hashtag['text'].lower())
         for hashtag in data['entities']['hashtags']
         if hashtag['text'].lower() not in hashtags]

        for hashtag in hashtags:
            conn.execute("INSERT INTO HASHTAGS (ID, HASHTAG) "
                         "VALUES (%i, '#%s');" %
                         (data['id'], hashtag))

    def insert_URLs(self, data):
        # We avoid repeated URLs
        urls = []
        [urls.append(url['expanded_url'])
         for url in data['entities']['urls']
         if url['expanded_url'] not in urls]

        for url in urls:
            conn.execute("INSERT INTO URLS (ID, URL) VALUES (%i,'%s');"
                         % (data['id'], url))

    def insert_Words(self, data):
        # Ignores punctuation
        text = ' '.join(word.strip(punctuation)
                        for word in data['text'].split()
                        if word.strip(punctuation))

        # We avoid inserting words that are irrelevant
        junkWords = [u'rt', u'a', u'the', u'an', u'this', u'that', u'these',
                     u'those', u'on', u'at', u'of', u'for', u'in', u'with',
                     u'to', u'by']

        # We want to avoid mixing urls with words
        urls = [url['url'] for url in data['entities']['urls']]

        # Compute a collection of all words from the tweet in lowercase
        words = [self.text_format(w).lower()
                 for w in text.split() if w.lower() not in junkWords
                 and w not in urls]

        # We avoid inserting repeated words in the same tweet
        insertion_words = []
        [insertion_words.append(word) for word in words
         if word not in insertion_words]

        # We insert the words into the database
        for word in insertion_words:
            conn.execute("INSERT INTO WORDS (ID, WORD) VALUES (%i,'%s');"
                         % (data['id'], word))

    def update_Retweet(self, data):
        # If the tweet was retweeted we update the stats of the original
        # tweet
        if 'retweeted_status' in data:
            conn.execute("UPDATE TWEETS "
                         "SET RTS = %i , FAVS = %i "
                         "WHERE ID = %i;"
                         % (data['retweeted_status']['retweet_count'],
                            data['retweeted_status']['favorite_count'],
                            data['retweeted_status']['id']))

    def extract_Time(self, data):
        # In this method we just split the data we want in a list
        info = {'id': data['id']}
        date = data['created_at'].split()
        info['dotw'] = date[0]
        info['month'] = date[1]
        info['day'] = int(date[2])
        # Special split for time hh:mm:ss
        hour = date[3].split(':')
        info['hour'] = int(hour[0])
        info['min'] = int(hour[1])
        info['sec'] = int(hour[2])
        return info

    def insert_Time(self, data):
        # We divide the data we are looking for in different fields in
        # an array and then we insert them into the database
        info = self.extract_Time(data)
        conn.execute("INSERT INTO TIME (ID_TWEET, DAY_OF_THE_WEEK, "
                     "DAY, MONTH, HOUR, MINUTE, SECOND) VALUES ( "
                     "%i, '%s', %i, '%s', %i, %i, %i);"
                     % (info['id'], info['dotw'], info['day'],
                        info['month'], info['hour'], info['min'],
                        info['sec']))

if __name__ == "__main__":

    # Verbose mode activation
    if "-v" in sys.argv:
        verbose = True
        print "Verbose mode ON"
    else:
        verbose = False
        print ("Verbose mode OFF. To activate it use -v "
               "parametter when excecuting")

    # Connection to DataBase
    conn = sqlite3.connect('db/tweetBank.db')
    if verbose:
        print "Opened database successfully"

    stream = MyStreamer(keys.CONSUMER_KEY, keys.CONSUMER_SECRET,
                        keys.OAUTH_TOKEN, keys.OAUTH_TOKEN_SECRET)
    keyword_list = 'beer'
    # Filter parameters can be found here:
    # https://dev.twitter.com/streaming/reference/post/statuses/filter
    stream.statuses.filter(track=keyword_list)
