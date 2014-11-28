from pytest import raises
from src.dbCreator import *
import os

db = 'db/test.db'

def test_tweetsTableCreator():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    tweetsTableCreator(conn)
    c.execute ("SELECT count(*) FROM sqlite_master "
            "WHERE type = 'table' and name = 'TWEETS'")

    result = c.fetchone()

    # Closing the connection
    conn.close()
    assert result[0] == 1


def test_usersTableCreator():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    usersTableCreator(conn)
    c.execute ("SELECT count(*) FROM sqlite_master "
            "WHERE type = 'table' and name = 'USERS'")

    result = c.fetchone()

    # Closing the connection
    conn.close()
    assert result[0] == 1


def test_timeTableCreator():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    timeTableCreator(conn)
    c.execute ("SELECT count(*) FROM sqlite_master "
            "WHERE type = 'table' and name = 'TIME'")

    result = c.fetchone()

    # Closing the connection
    conn.close()
    assert result[0] == 1


def test_hashtagsTableCreator():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    hashtagsTableCreator(conn)
    c.execute ("SELECT count(*) FROM sqlite_master "
            "WHERE type = 'table' and name = 'HASHTAGS'")

    result = c.fetchone()

    # Closing the connection
    conn.close()
    assert result[0] == 1


def test_urlsTableCreator():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    urlsTableCreator(conn)
    c.execute ("SELECT count(*) FROM sqlite_master "
            "WHERE type = 'table' and name = 'URLS'")

    result = c.fetchone()

    # Closing the connection
    conn.close()
    assert result[0] == 1


def test_wordTableCreator():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    wordTableCreator(conn)
    c.execute ("SELECT count(*) FROM sqlite_master "
            "WHERE type = 'table' and name = 'WORDS'")

    result = c.fetchone()

    # Closing the connection
    conn.close()
    assert result[0] == 1


def test_producesTableCreator():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    producesTableCreator(conn)
    c.execute ("SELECT count(*) FROM sqlite_master "
            "WHERE type = 'table' and name = 'PRODUCES'")

    result = c.fetchone()

    # Closing the connection
    conn.close()
    assert result[0] == 1

def test_mentionsTableCreator():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    mentionsTableCreator(conn)
    c.execute ("SELECT count(*) FROM sqlite_master "
            "WHERE type = 'table' and name = 'MENTIONS'")

    result = c.fetchone()

    # Closing the connection
    conn.close()
    assert result[0] == 1

def test_indexCreator():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    indexCreator(conn)
    c.execute ("SELECT count(*) FROM sqlite_master"
            " WHERE type = 'index' and name = 'GEO'")

    result = c.fetchone()

    # Closing the connection
    conn.close()
    assert result[0] == 1


#def test_removeDB():
    """
    This method is not in the original module. But it is neccesary 
    if we want to remove the db for the followings tests.
    """
 #   os.remove(db)


