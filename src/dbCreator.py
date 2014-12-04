import sqlite3
import sys

verbose = False

def tweetsTableCreator(conn):
    # Creating main tables
    conn.execute('''CREATE TABLE TWEETS
        (ID INT PRIMARY KEY NOT NULL,
        TWEET_TEXT CHAR(140) NOT NULL,
        FAVS INT NOT NULL,
        RTS INT NOT NULL,
        LAT REAL,
        LONG REAL,
        FOLLOWERS INT);''')

    if verbose:
        print ("Table Tweets created successfully")

def usersTableCreator(conn):
    # If verified equals to one means it is true, zero means it is false
    conn.execute('''CREATE TABLE USERS
        (ID INT PRIMARY KEY NOT NULL,
        SCREEN_NAME TEXT NOT NULL,
        NAME TEXT NOT NULL,
        VERIFIED INT NOT NULL,
        LANG TEXT);''')

    if verbose:
        print ("Table Users created successfully")

def timeTableCreator(conn):
    # Table for tweets timing
    conn.execute('''CREATE TABLE TIME
        (ID_TWEET INT PRIMARY KEY NOT NULL,
        DAY_OF_THE_WEEK TEXT NOT NULL,
        DAY INT NOT NULL,
        MONTH TEXT NOT NULL,
        HOUR INT NOT NULL,
        MINUTE INT NOT NULL,
        SECOND INT NOT NULL,
        FOREIGN KEY (ID_TWEET) REFERENCES TWEETS(ID));''')

    if verbose:
        print ("Table Time created successfully")

def hashtagsTableCreator(conn):
    # Creating tables for multivaluated attributes for some tables
    conn.execute('''CREATE TABLE HASHTAGS
        (HASHTAG TEXT NOT NULL COLLATE NOCASE,
        ID INT NOT NULL,
        FOREIGN KEY (ID) REFERENCES TWEETS(ID),
        PRIMARY KEY (HASHTAG, ID));''')

    if verbose:
        print ("Table Hashtags created successfully")

def urlsTableCreator(conn):
    conn.execute('''CREATE TABLE URLS
        (URL TEXT NOT NULL,
        ID INT NOT NULL,
        FOREIGN KEY (ID) REFERENCES TWEETS(ID),
        PRIMARY KEY (URL, ID));''')

    if verbose:
        print ("Table Hashtags created successfully")

def wordTableCreator(conn):
    conn.execute('''CREATE TABLE WORDS
        (WORD TEXT NOT NULL COLLATE NOCASE,
        ID INT NOT NULL,
        FOREIGN KEY (ID) REFERENCES TWEETS(ID),
        PRIMARY KEY (WORD, ID));''')

    if verbose:
        print ("Table Words created successfully")

def producesTableCreator(conn):
    # PRODUCES --> A user produces many tweets
    conn.execute('''CREATE TABLE PRODUCES
        (ID_TWEET INT NOT NULL,
        ID_USER INT NOT NULL,
        FOREIGN KEY (ID_TWEET) REFERENCES TWEETS(ID),
        FOREIGN KEY (ID_USER) REFERENCES USERS(ID),
        PRIMARY KEY (ID_USER, ID_TWEET));''')

    if verbose:
        print ("Table Produces created successfully")

def mentionsTableCreator(conn):
    # MENTIONS --> A tweet mentions many users
    conn.execute('''CREATE TABLE MENTIONS
        (ID_TWEET INT NOT NULL,
        ID_USER INT NOT NULL,
        FOREIGN KEY (ID_TWEET) REFERENCES TWEETS(ID),
        FOREIGN KEY (ID_USER) REFERENCES USERS(ID),
        PRIMARY KEY (ID_USER, ID_TWEET));''')

    if verbose:
        print ("Table Mentions created successfully")

def indexCreator(conn):
    # Index to search easily by geo-position
    conn.execute("CREATE INDEX GEO ON TWEETS(LAT, LONG);")

    if verbose:
        print ("Index GEO created successfully")

if __name__ == "__main__":

    # Verbose mode activation
    if "-v" in sys.argv:
        verbose = True
        print ("Verbose mode ON.")
    else:
        verbose = False
        print ("Verbose mode OFF. To activate it use -v parametter when excecuting")

    # Connection to DataBase
    con = sqlite3.connect('db/tweetBank.db')
    if verbose:
        print ("Opened database successfully")

    # Creating main tables
    tweetsTableCreator(con)
    usersTableCreator(con)

    # Creating tables for relations between main tables
    timeTableCreator(con)
    hashtagsTableCreator(con)
    urlsTableCreator(con)
    wordTableCreator(con)
    producesTableCreator(con)
    mentionsTableCreator(con)

    # Creating indexes
    indexCreator(con)
    # Closing the connection
    con.close()
