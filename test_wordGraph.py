from pytest import raises
from src.wordGraph import *

db = 'db/test.db'

def test_text_format():
    assert text_format("asdkjhaeih") == "asdkjhaeih"
    assert text_format("as&amp;dkj&gt;hae&lt;ih") == "as&dkj>hae<ih"
    assert text_format("") == ""

def test_correct_position ():
    # Creation of the matrix
    matrix = defaultdict(dict)
    matrix ["a"] ["b"] = 0
    assert correct_position (matrix, "a", "b") == ["a", "b"]
    assert correct_position (matrix, "b", "a") == ["a", "b"]
    assert correct_position (matrix, "c", "a") == None

def test_create_position ():
    # Creation of the matrix
    matrix = defaultdict(dict)
    wordA = "a"
    wordB = "b"
    assert ["a", "b"] == create_position (matrix, wordA, wordB)
    assert matrix [wordA] [wordB] == 0
    
def test_bound (): 
    conn = sqlite3.connect(db)

    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", LAT, LONG, FOLLOWERS) "
                 "VALUES(0, 'test2 test0',0 , 0,-5.6, 6.12, 0)")
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(1, 'test2 test0',0 , 0, 0)")
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(2, 'test2',0 , 0, 0)")

    c = conn.cursor()

    bound0 = round(bound(c, "0.3"),1)
    bound1 = bound(c, "0")
    bound2 = bound(c, "1")

    conn.execute("DELETE FROM TWEETS WHERE ID=0")
    conn.execute("DELETE FROM TWEETS WHERE ID=1")
    conn.execute("DELETE FROM TWEETS WHERE ID=2")

    # Closing the connection
    conn.close()

    assert bound0 == 2.1
    assert bound1 == 3
    assert bound2 == 0

def test_readTweets():
    conn = sqlite3.connect(db)

    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", LAT, LONG, FOLLOWERS) "
                 "VALUES(0, 'test2 test0',0 , 0,-5.6, 6.12, 0)")
    conn.execute("INSERT INTO WORDS (ID, WORD) VALUES (0,'test2')")
    conn.execute("INSERT INTO WORDS (ID, WORD) VALUES (0,'test0')")

    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(1, 'test2 test0',0 , 0, 0)")
    conn.execute("INSERT INTO WORDS (ID, WORD) VALUES (1,'test2')")
    conn.execute("INSERT INTO WORDS (ID, WORD) VALUES (1,'test0')")

    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(2, 'test2',0 , 0, 0)")
    conn.execute("INSERT INTO WORDS (ID, WORD) VALUES (2,'test2')")

    c = conn.cursor()

    tweet_list0 = readTweets(c, "1")
    tweet_list1 = readTweets(c, "0")
    tweet_list2 = readTweets(c, "0.7")

    conn.execute("DELETE FROM TWEETS WHERE ID=0")
    conn.execute("DELETE FROM TWEETS WHERE ID=1")
    conn.execute("DELETE FROM TWEETS WHERE ID=2")

    # Closing the connection
    conn.close()

    assert (0 in tweet_list0) and (1 in tweet_list0) and (2 in tweet_list0)
    assert tweet_list1 == []
    assert (0 in tweet_list2) and (1 in tweet_list2)

def test_matchWords():
    conn = sqlite3.connect(db)

    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", LAT, LONG, FOLLOWERS) "
                 "VALUES(0, 'a b c',0 , 0,-5.6, 6.12, 0)")
    conn.execute("INSERT INTO WORDS (ID, WORD) VALUES (0,'a')")
    conn.execute("INSERT INTO WORDS (ID, WORD) VALUES (0,'b')")
    conn.execute("INSERT INTO WORDS (ID, WORD) VALUES (0,'c')")

    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(1, 'test2 test0',0 , 0, 0)")
    conn.execute("INSERT INTO WORDS (ID, WORD) VALUES (1,'test2')")
    conn.execute("INSERT INTO WORDS (ID, WORD) VALUES (1,'test0')")

    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(2, 'test2 c',0 , 0, 0)")
    conn.execute("INSERT INTO WORDS (ID, WORD) VALUES (2,'test2')")
    conn.execute("INSERT INTO WORDS (ID, WORD) VALUES (2,'c')")

    c = conn.cursor()
    tweet_list = [0,1,2]

    matrix = matchWords(c, tweet_list)

    conn.execute("DELETE FROM TWEETS WHERE ID=0")
    conn.execute("DELETE FROM TWEETS WHERE ID=1")
    conn.execute("DELETE FROM TWEETS WHERE ID=2")

    # Closing the connection
    conn.close()    

    try:
        assert (matrix["a"] ["b"] == 1)
    except:
        assert(matrix["b"] ["a"] == 1)
    try:
        assert (matrix["a"] ["c"] == 1)
    except:
        assert (matrix["c"] ["a"] == 1)
    try:
        assert (matrix["b"] ["c"] == 1)
    except:
        assert (matrix["c"] ["b"] == 1)

    try:
        assert (matrix["test2"] ["test0"] == 1)
    except:
        assert (matrix["test0"] ["test2"] == 1)
    try:
        assert (matrix["test2"] ["c"] == 1)
    except:
        assert (matrix["c"] ["test 2"] == 1)
