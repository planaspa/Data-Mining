from src.graphDb import *

db = 'db/test.db'


def test_text_format():
    assert text_format("asdkjhaeih") == "asdkjhaeih"
    assert text_format("as&amp;dkj&gt;hae&lt;ih") == "as&dkj>hae<ih"
    assert text_format("") == ""


def test_creatingGroups():

    conn = sqlite3.connect(db)

    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", LAT, LONG, FOLLOWERS) "
                 "VALUES(0, 'test2 test0',0 , 0,-5.6, 6.12, 105)")
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(1, 'test2 test0',0 , 0, 5)")
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(2, 'test2',0 , 0, 30)")

    c = conn.cursor()

    groups1 = creatingGroups(c, 2)
    groups2 = creatingGroups(c, 4)

    conn.execute("DELETE FROM TWEETS WHERE ID=0")
    conn.execute("DELETE FROM TWEETS WHERE ID=1")
    conn.execute("DELETE FROM TWEETS WHERE ID=2")

    # Closing the connection
    conn.close()

    assert groups1 == [5, 55, 105]
    assert groups2 == [5, 30, 55, 80, 105]


def test_numberOfTweetsPerGroup():

    conn = sqlite3.connect(db)

    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", LAT, LONG, FOLLOWERS) "
                 "VALUES(0, 'test2 test0',0 , 0,-5.6, 6.12, 105)")
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(1, 'test2 test0',0 , 0, 5)")
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(2, 'test2',0 , 0, 30)")

    c = conn.cursor()

    groups1 = creatingGroups(c, 2)
    groups2 = creatingGroups(c, 4)

    tweetsPerGroup1 = numberOfTweetsPerGroup(c, groups1)
    tweetsPerGroup2 = numberOfTweetsPerGroup(c, groups2)

    conn.execute("DELETE FROM TWEETS WHERE ID=0")
    conn.execute("DELETE FROM TWEETS WHERE ID=1")
    conn.execute("DELETE FROM TWEETS WHERE ID=2")

    # Closing the connection
    conn.close()

    assert tweetsPerGroup1 == [1, 1]
    assert tweetsPerGroup2 == [1, 0, 0, 1]


def test_numberOfReTweetsPerGroup():

    conn = sqlite3.connect(db)

    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", LAT, LONG, FOLLOWERS) "
                 "VALUES(0, 'test2 test0',5 , 5,-5.6, 6.12, 105)")
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(1, 'test2 test0',0 , 0, 5)")
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(2, 'test2',3 , 3, 30)")

    c = conn.cursor()

    groups1 = creatingGroups(c, 2)
    groups2 = creatingGroups(c, 4)

    rtsPerGroup1 = numberOfReTweetsPerGroup(c, groups1)
    rtsPerGroup2 = numberOfReTweetsPerGroup(c, groups2)

    conn.execute("DELETE FROM TWEETS WHERE ID=0")
    conn.execute("DELETE FROM TWEETS WHERE ID=1")
    conn.execute("DELETE FROM TWEETS WHERE ID=2")

    # Closing the connection
    conn.close()

    assert rtsPerGroup1 == [3, 5]
    assert rtsPerGroup2 == [3, 0, 0, 5]


def test_numberOfFavsPerGroup():

    conn = sqlite3.connect(db)

    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", LAT, LONG, FOLLOWERS) "
                 "VALUES(0, 'test2 test0',5 , 5,-5.6, 6.12, 105)")
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(1, 'test2 test0',0 , 0, 5)")
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(2, 'test2',3 , 3, 30)")

    c = conn.cursor()

    groups1 = creatingGroups(c, 2)
    groups2 = creatingGroups(c, 4)

    favsPerGroup1 = numberOfFavsPerGroup(c, groups1)
    favsPerGroup2 = numberOfFavsPerGroup(c, groups2)

    conn.execute("DELETE FROM TWEETS WHERE ID=0")
    conn.execute("DELETE FROM TWEETS WHERE ID=1")
    conn.execute("DELETE FROM TWEETS WHERE ID=2")

    # Closing the connection
    conn.close()

    assert favsPerGroup1 == [3, 5]
    assert favsPerGroup2 == [3, 0, 0, 5]
