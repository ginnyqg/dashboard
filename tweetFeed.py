from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from unidecode import unidecode


conn = sqlite3.connect('twitter.db')
c = conn.cursor()

def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS CAtweets(unix REAL, tweet TEXT)")
	conn.commit()
create_table()


ckey = ''
csecret = ''
atoken = ''
asecret = ''

class listener(StreamListener):

	def on_data(self, data):
		try:
			data = json.loads(data)
			tweet = unidecode(data['text'])
			time_ms = data['timestamp_ms']
			print(time_ms, tweet)
			c.execute("INSERT INTO CAtweets (unix, tweet) VALUES (?, ?)", (time_ms, tweet))
			conn.commit()

		except KeyError as e:
			print(str(e))

		return True


	def on_error(self, status):
		print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track = ['#techacquisition', '#tech', '#technology', '#merger'])




