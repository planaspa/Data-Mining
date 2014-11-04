"""
Created on Sat Nov  1 19:13:31 2014

@author: Mia

Corrected by planaspa
"""
import sqlite3
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


def text_format(text):
    text = text.replace("&amp;","&")
    text = text.replace("&gt;",">")
    text = text.replace("&lt;","<")
    return text


conn = sqlite3.connect('db/tweetBank.db')
c = conn.cursor()

# select retweets from TWEETS table and save in different arrays to plot later
c.execute("SELECT TWEET_TEXT, FOLLOWERS, RTS FROM TWEETS")
cursor = list(c)
ttext = [text_format(record[0]) for record in cursor]
length_text = [len(text) for text in ttext]
rts = [int(record[1]) for record in cursor]
flws = [int(record[2]) for record in cursor]



# Useful code to find special characters in tweets
for text in ttext:
    if len(text) > 140:
        print (len(text))
        print (text)

    
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(rts,flws,length_text, c='r', marker='o')

ax.set_xlabel('Followers')
ax.set_ylabel('Retweets')
ax.set_zlabel('Characters per tweet')

plt.show()
