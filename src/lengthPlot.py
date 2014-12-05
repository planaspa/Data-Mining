import sqlite3
import matplotlib.pyplot as plt


def text_format(text):
    text = text.replace("&amp;", "&")
    text = text.replace("&gt;", ">")
    text = text.replace("&lt;", "<")
    return text


def loadData(c):
    c.execute("SELECT TWEET_TEXT, RTS, FAVS FROM TWEETS")
    cursor = list(c)
    tweetInfo = [(len(text_format(record[0])), record[1], record[2])
                 for record in cursor]
    return tweetInfo


def spreadInfo(tweetInfo):
    rtsPerTweet = [0] * 141
    favsPerTweet = [0] * 141
    numberOfTweet = [0] * 141

    for tweet in tweetInfo:
        rtsPerTweet[tweet[0]] += tweet[1]
        favsPerTweet[tweet[0]] += tweet[2]
        numberOfTweet[tweet[0]] += 1

    return [rtsPerTweet, favsPerTweet, numberOfTweet]

if __name__ == "__main__":
    print ("Connecting to database...")
    conn = sqlite3.connect('db/tweetBank.db')
    c = conn.cursor()

    print ("Loading data...")
    tweetInfo = loadData(c)

    # Closing the connection
    conn.close()

    print ("Doing some calculations...")
    info = spreadInfo(tweetInfo)

    rtsPerTweet = info[0]
    favsPerTweet = info[1]
    numberOfTweet = info[2]

    rtsAverage = [float(rt)/length if length != 0 else 0
                  for rt, length in zip(rtsPerTweet, numberOfTweet)]
    favsAverage = [float(fav)/length if length != 0 else 0
                   for fav, length in zip(favsPerTweet, numberOfTweet)]

    fig, ax = plt.subplots()
    # Minimum 7 to avoid seeing the points of 0 retweets and
    # a little bit more in the max
    plt.xlabel("Number of characters in a tweet")
    plt.ylabel("Average of interactions")
    lineRts, = ax.plot(range(141), rtsAverage, alpha=0.5,
                       label='average Rts', color='green')
    lineFavs, = ax.plot(range(141), favsAverage, alpha=0.5,
                        label='average Favs', color='orange')
    first_legend = plt.legend(handles=[lineRts, lineFavs], loc=1)
    ax = plt.gca().add_artist(first_legend)

    fig2, ax2 = plt.subplots()
    line, = ax2.plot(range(141), numberOfTweet, alpha=0.5,
                     label='amountOfTweets')
    plt.xlabel("Number of characters in a tweet")
    plt.ylabel("Amount of tweets gathered")
    second_legend = plt.legend(handles=[line], loc=1)
    ax2 = plt.gca().add_artist(second_legend)
    plt.show()
