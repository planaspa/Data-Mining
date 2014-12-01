import sqlite3
import matplotlib.pyplot as plt
import sys


def text_format(text):
    text = text.replace("&amp;","&")
    text = text.replace("&gt;",">")
    text = text.replace("&lt;","<")
    return text

def creatingGroups(c, nGroups):
    """
    This function returns a list which divides the tweets in different
    groups, depending on their number of followers.
    """
    # We calculate the maximum number of followers for a tweet in the db
    c.execute("SELECT MAX(FOLLOWERS) FROM TWEETS")
    result = c.fetchone()
    maxFollowers = result[0]

    # We calculate the minimum number of followers for a tweet in the db
    c.execute("SELECT MIN(FOLLOWERS) FROM TWEETS")
    result = c.fetchone()
    minFollowers = result[0]

    groups = range(minFollowers, maxFollowers, maxFollowers/nGroups)
    groups.append(maxFollowers)
    return groups

def numberOfTweetsPerGroup(c, groups):
    
    tweetsPerGroup=[]
    for pair in zip(groups, groups[1:]):
        c.execute("SELECT COUNT(*) FROM TWEETS WHERE FOLLOWERS > %i AND " 
                  "FOLLOWERS <= %i" %(pair[0], pair[1]))
        result = c.fetchone()
        tweetsPerGroup.append(result[0])

    return tweetsPerGroup

def numberOfReTweetsPerGroup(c, groups):
    
    rtsPerGroup=[]
    for pair in zip(groups, groups[1:]):
        c.execute("SELECT SUM(RTS) FROM TWEETS WHERE FOLLOWERS > %i AND " 
                  "FOLLOWERS <= %i" %(pair[0], pair[1]))
        result = c.fetchone()
        if result[0] is None:
            rtsPerGroup.append(0)
        else:
            rtsPerGroup.append(result[0])

    return rtsPerGroup

def numberOfFavsPerGroup(c, groups):
    
    favsPerGroup=[]
    for pair in zip(groups, groups[1:]):
        c.execute("SELECT SUM(FAVS) FROM TWEETS WHERE FOLLOWERS > %i AND " 
                  "FOLLOWERS <= %i" %(pair[0], pair[1]))
        result = c.fetchone()
        if result[0] is None:
            favsPerGroup.append(0)
        else:
            favsPerGroup.append(result[0])

    return favsPerGroup
    
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "I need a number of groups as an argument"
        sys.exit()

    conn = sqlite3.connect('db/tweetBank.db')
    c = conn.cursor()

    print "Loading Groups..."
    groups= creatingGroups(c, int(sys.argv[1]))
    print "Loading Tweets..."
    tweets = numberOfTweetsPerGroup(c, groups)
    print "Loading Retweets..."
    rts = numberOfReTweetsPerGroup(c, groups)
    print "Loading Favourites..."
    favs = numberOfFavsPerGroup(c, groups)
    print "Doing some calculations..."
    rtsPerTweets = [float(rt)/tweet if tweet!=0 else 0 for rt, tweet in zip(rts, tweets)]
    favsPerTweets = [float(fav)/tweet if tweet!=0 else 0 for fav, tweet in zip(favs, tweets)]

    fig, ax = plt.subplots()
    # Minimum 7 to avoid seeing the points of 0 retweets and a little bit more in the max
    ax.set_ylim([7,max(rtsPerTweets)+100])
    ax.plot(groups[1:], rtsPerTweets, marker='o', linestyle='None', color='green')
    ax.plot(groups[1:], favsPerTweets, marker='o', linestyle='None', color='orange')
    plt.show() 
