from pytest import raises
from src.lengthPlot import *

db = 'db/test.db'

def test_text_format():
    assert text_format("asdkjhaeih") == "asdkjhaeih"
    assert text_format("as&amp;dkj&gt;hae&lt;ih") == "as&dkj>hae<ih"
    assert text_format("") == ""

def test_loadData():
    conn = sqlite3.connect(db)
    
    c = conn.cursor()
    tweetInfo = loadData(c)
    
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", LAT, LONG, FOLLOWERS) "
                 "VALUES(0, 'test2 test0',7 , 5,-5.6, 6.12, 105)")
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(1, 'test2 test0',0 , 0, 5)")
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(2, 'test2',3 , 3, 30)")

    tweetInfo2 = loadData(c)

    conn.execute("DELETE FROM TWEETS WHERE ID=0")
    conn.execute("DELETE FROM TWEETS WHERE ID=1")
    conn.execute("DELETE FROM TWEETS WHERE ID=2")

    # Closing the connection
    conn.close()

    assert tweetInfo == []
    assert tweetInfo2 == [(11,5,7),(11,0,0),(5,3,3)]

def test_spreadInfo():
    tweetInfo = [(11,5,7),(11,0,0),(5,3,3)]
    info = spreadInfo(tweetInfo)

    rtsPerTweet = info[0]
    favsPerTweet = info[1]
    numberOfTweet = info[2]
    
    testRts = [0] * 141
    testFavs = [0] * 141
    testNumber = [0] * 141
    
    testRts[5] = 3
    testRts[11] = 5

    testFavs[5] = 3
    testFavs[11] = 7

    testNumber[5] = 1
    testNumber[11] = 2

    assert rtsPerTweet == testRts
    assert favsPerTweet == testFavs
    assert numberOfTweet  == testNumber
