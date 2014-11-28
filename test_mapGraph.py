from pytest import raises
from src.mapGraph import *

db = 'db/test.db'

def test_loadDataEmptyDatabase():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    coordinates = loadData(conn)
    # Closing the connection
    conn.close()
    assert len(coordinates) == 2
    assert len(coordinates[0]) == 0
    assert len(coordinates[1]) == 0

def test_loadDataWithData():
    conn = sqlite3.connect(db)
    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", LAT, LONG, FOLLOWERS) "
                 "VALUES(0, 'test',0 , 0,-5.6, 6.12, 0)")

    conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS"
                 ", FOLLOWERS) "
                 "VALUES(1, 'test',0 , 0, 0)")

    coordinates = loadData(conn)

    conn.execute("DELETE FROM TWEETS WHERE ID=0")
    conn.execute("DELETE FROM TWEETS WHERE ID=1")

    # Closing the connection
    conn.close()
    assert len(coordinates) == 2
    assert coordinates[0] == [-5.6]
    assert coordinates[1] == [6.12]
    
