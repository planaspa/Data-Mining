import sqlite3
import sys

# Verbose mode activation
if "-v" in sys.argv:
	verbose = True
	print "Verbose mode ON."
else:
	verbose = False
	print "Verbose mode OFF. To activate it use -v parametter when excecuting"


#Connection to DataBase
conn = sqlite3.connect('../db/tweetBank.db')
if verbose : print "Opened database successfully"

# Creating main tables
conn.execute('''CREATE TABLE TWEETS
       (ID INT PRIMARY KEY NOT NULL,
       TWEET_TEXT CHAR(140) NOT NULL,
       FAVS INT NOT NULL,
       RTS INT NOT NULL,
       LAT REAL,
       LONG REAL);''')

if verbose : print "Table Tweets created successfully"

conn.execute('''CREATE TABLE USERS
       (ID INT PRIMARY KEY NOT NULL,
       SCREEN_NAME TEXT NOT NULL,
       NAME TEXT NOT NULL,
       VERIFIED INT NOT NULL, 
       LANG TEXT);''') #If verified equals to one means it is true, zero means it is false

if verbose : print "Table Users created successfully"

# Creating tables for multivaluated attributes for some tables
conn.execute('''CREATE TABLE HASHTAGS
       (HASHTAG TEXT NOT NULL,
        ID INT NOT NULL,
	FOREIGN KEY (ID) REFERENCES TWEETS(ID),
        PRIMARY KEY (HASHTAG, ID));''')

if verbose : print "Table Hashtags created successfully"

conn.execute('''CREATE TABLE URLS
       (URL TEXT NOT NULL,
        ID INT NOT NULL,
	FOREIGN KEY (ID) REFERENCES TWEETS(ID),
        PRIMARY KEY (URL, ID));''')

if verbose : print "Table Hashtags created successfully"

# Creating tables for relations between main tables
# PRODUCES --> A user produces many tweets
conn.execute('''CREATE TABLE PRODUCES
       (ID_TWEET INT NOT NULL,
        ID_USER INT NOT NULL,
	FOREIGN KEY (ID_TWEET) REFERENCES TWEETS(ID),
	FOREIGN KEY (ID_USER) REFERENCES USERS(ID),
        PRIMARY KEY (ID_USER, ID_TWEET));''')

if verbose : print "Table Produces created successfully"

# MENTIONS --> A tweet mentions many users
conn.execute('''CREATE TABLE MENTIONS
       (ID_TWEET INT NOT NULL,
        ID_USER INT NOT NULL,
	FOREIGN KEY (ID_TWEET) REFERENCES TWEETS(ID),
	FOREIGN KEY (ID_USER) REFERENCES USERS(ID),
        PRIMARY KEY (ID_USER, ID_TWEET));''')

if verbose : print "Table Mentions created successfully"
