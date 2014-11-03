# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 19:13:31 2014

@author: Mia
"""

# NOTE: I still haven't fixed the decoding.

from __future__ import unicode_literals
import sqlite3
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
#import chardet

conn = sqlite3.connect('tweetBank.db')
c = conn.cursor()

rts = []
flws = []
ttext = []

# select retweets from TWEETS table and save in an array to plot later
c.execute("SELECT RTS FROM TWEETS")
rts = [int(record[0]) for record in c.fetchall()]
   # rt = int(str(retweets).replace(')','').replace('(','').replace('u\'','').replace("'","").replace(",",""))
   # rts.append(rt)
    #print(retweets)
#print (rts)

#Make and array of followers
c.execute("SELECT FOLLOWERS FROM TWEETS")
flws = [int(record[0]) for record in c.fetchall()]

    
#print (flws)
    


# Makes an array of tweets (text). Decoding isn't working.
c.execute("SELECT TWEET_TEXT FROM TWEETS")
print (type(c.fetchone()[0]))
ttext = [record[0] for record in c.fetchall()]
#ttext = [unicode(record[0], chardet.detect(record[0])['encoding']).encode('ascii', 'ignore') for record in c.fetchall()]
for t in ttext:
    print(t)
    
#print(ttext)
 #   ttext.append(str(twitter_text))
  #  print(twitter_text)
#print (rts, flws)
"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
"""
Z = []
i = 0
while (i < len(ttext)):
    Z.append(len(ttext[i]))
    if (len(ttext[i]) > 140):
        print (Z[i])
        print (ttext[i])
    i+=1
    
"""
ax.scatter(rts,flws,Z, c='r', marker='o')

ax.set_xlabel('Retweets')
ax.set_ylabel('Followers')
ax.set_zlabel('Nr of Characters in tweet')

plt.show()"""
