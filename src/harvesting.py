from twython import TwythonStreamer
import keys


class MyStreamer(TwythonStreamer):
	"""
	Setting up the streamer. Defining how to handle the signals that Twython Streamer API uses.  
	"""   
	def on_success(self, data):
		if 'text' in data:
			print data['text'].encode('utf-8')

	def on_error(self, status_code, data):
		print status_code

        # Wanting to insist to get the data even having an error?
        # Comment the next line!
		self.disconnect()

	def on_timeout():
		print '*** ERROR ***: The request has timed out.'





stream = MyStreamer(keys.CONSUMER_KEY, keys.CONSUMER_SECRET,
                    keys.OAUTH_TOKEN, keys.OAUTH_TOKEN_SECRET)
keyword_list = ['beer']

for keyword in keyword_list:
	# Filter parameters can be found here: https://dev.twitter.com/streaming/reference/post/statuses/filter
	stream.statuses.filter(track=keyword)

