from twython import TwythonStreamer
import keys
import sqlite3
import sys

class MyStreamer(TwythonStreamer):
	"""
	Setting up the streamer. Defining how to handle the signals that Twython Streamer API uses.  
	"""   
	def on_success(self, data):
	
		# Just to have the count of how many tweets we are storing in the db while harversting
		cursor = conn.cursor()
		cursor.execute("SELECT COUNT(*) FROM TWEETS;")
		result=cursor.fetchone()
		successful_tweets = result[0]

		# We only take tweets that are in English
		if data['lang'] == 'en':
			#Inserting into Tweets Table depending on whether we coordinates exist or not
			if data['coordinates'] == None:
				conn.execute("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS) " 
					"VALUES (%i, '%s', %i, %i);" %(data['id'], data['text'].replace("'","''"), 
							data['favorite_count'], data['retweet_count']))
				conn.commit()
				
			else:
				if data['coordinates']['type'] == 'Point':
					conn.execute ("INSERT INTO TWEETS(ID, TWEET_TEXT, FAVS, RTS, LAT, LONG) "
							"VALUES (%i, '%s', %i, %i, %f, %f);" %(data['id'], 
								data['text'].replace("'","''"), 
								data['favorite_count'], data['retweet_count'],
								data['coordinates']['coordinates'][1], 
								data['coordinates']['coordinates'][0]))
					conn.commit()
			#Inserting into Users Table
			if data['user']['verified'] == "True":
				verified = 1
			else:
				verified = 0
			
			# We have to see whether the user has already been stored or not
			cursor.execute("SELECT COUNT(*) FROM USERS WHERE ID=%s;" %data['user']['id'])
			result=cursor.fetchone()
			if result[0] == 0:
				conn.execute("INSERT INTO USERS(ID, NAME, SCREEN_NAME, VERIFIED, LANG) " 
					"VALUES (%i, '%s', '%s', %i, '%s');" %(data['user']['id'], data['user']['name'].replace("'","''"), 
							data['user']['screen_name'].replace("'","''"), verified,data['user']['lang']))
				conn.commit()

			#Inserting into Produces Table
			conn.execute("INSERT INTO PRODUCES(ID_TWEET, ID_USER) " 
				"VALUES (%i, %i);" %(data['id'], data['user']['id']))
			conn.commit()

			#Inserting into Mentions Table
			for user in data['entities']['user_mentions']:
				try:
					conn.execute ("INSERT INTO MENTIONS (ID_TWEET, ID_USER) "
							"VALUES (%i, %i);" %(data['id'],user['id']))
					conn.commit()
				except sqlite3.IntegrityError:
					# The exception may be caused because the same tweet mentions twice or more times
					# a single user, we are going to check it. If it happens we just ignore it, otherwise not.
					cursor.execute("SELECT COUNT(*) FROM MENTIONS WHERE ID_TWEET=%i " \
							"AND ID_USER=%i;" %(data['id'],user['id']))
					result=cursor.fetchone()					
					if result[0] > 0:
						pass
					else: 
						print "*** Error was caused by the following tweet ***"
						print data
						break

			#Inserting into Hashtags Table
			for hashtag in data['entities']['hashtags']:
				try:
					conn.execute ("INSERT INTO HASHTAGS (ID, HASHTAG) "
							"VALUES (%i, '#%s');" %(data['id'],hashtag['text']))
					conn.commit()
				except sqlite3.IntegrityError:
					# The exception may be caused because the same tweet has the same hashtag twice or 
					# more times, we are going to check it. If it happens we just ignore it, otherwise not.
					cursor.execute("SELECT COUNT(*) FROM HASHTAGS WHERE ID=%i " \
							"AND HASHTAG='%s';" %(data['id'],hashtag['text']))
					result=cursor.fetchone()					
					if result[0] > 0:
						pass
					else: 
						print "*** Error was caused by the following tweet ***"
						print data
						break			

			#Inserting into URLs Table
			for url in data['entities']['urls']:
				try:
					conn.execute ("INSERT INTO URLS (ID, URL) "
						"VALUES (%i, '%s');" %(data['id'],url['expanded_url']))
					conn.commit()
				except sqlite3.IntegrityError:
					# The exception may be caused because the same tweet has the same URL twice or 
					# more times, we are going to check it. If it happens we just ignore it, otherwise not.
					cursor.execute("SELECT COUNT(*) FROM URLS WHERE ID=%i " \
							"AND URL='%s';" %(data['id'],url['expanded_url']))
					result=cursor.fetchone()					
					if result[0] > 0:
						pass
					else: 
						print "*** Error was caused by the following tweet ***"
						print data
						break	
			# We show the count
			successful_tweets += 1
			print "%i tweets inserted succesfully." %successful_tweets




	def on_error(self, status_code, data):
		print status_code

        # Wanting to insist to get the data even having an error?
        # Comment the next line!
		self.disconnect()

	def on_timeout():
		print '*** ERROR ***: The request has timed out.'

# Verbose mode activation
if "-v" in sys.argv:
	verbose = True
	print "Verbose mode ON"
else:
	verbose = False
	print "Verbose mode OFF. To activate it use -v parametter when excecuting"


#Connection to DataBase
conn = sqlite3.connect('../db/tweetBank.db')
if verbose : print "Opened database successfully"


stream = MyStreamer(keys.CONSUMER_KEY, keys.CONSUMER_SECRET,
                    keys.OAUTH_TOKEN, keys.OAUTH_TOKEN_SECRET)
keyword_list = ['beer']
stream.statuses.filter(track='beer')
"""
for keyword in keyword_list:
	# Filter parameters can be found here: https://dev.twitter.com/streaming/reference/post/statuses/filter
	stream.statuses.filter(track=keyword)
"""

