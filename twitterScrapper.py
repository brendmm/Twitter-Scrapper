import tweepy
from threading import Thread
import time
from tweepy.streaming import StreamListener
import smtplib
import config
import re

def clean(text):
    print("Cleaning Text")
    newText=''
    for char in text:
        if ord(char) >= 32 and ord(char) <=126:
            newText = newText+ char
    return newText

def send_email(sub,msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.email,config.password)
        message="Subject: {}\n\n{}".format(sub,msg)
        server.sendmail(config.email,config.dest1,message)
        server.sendmail(config.email,config.dest2,message)
        server.quit()
        print('Email sent') 
    except:
        print('Email failed to send') 
# bearer token = 'AAAAAAAAAAAAAAAAAAAAAA3gRwEAAAAAvlFP%2BWFRlmPj08AaM%2BkouPbciNk%3DyZg3v0kSFc2YLucg27aRD7Z4inZ1rIJNcV1p0sIEy0B95bI6lx'

consumer_key = 'mRUSaSFxBZPqrP9fRkPBwOyts'
consumer_secret = 'r0b4fWInb5XLC80mPKv3nnKSANtKEBJoLzP4srgagljZalX4Dy'
access_token = '1227784400684879880-s3GhKPw6E2vxfNiMzRwmbZLwBh71yP'
access_token_secret = 'MRtLvygQPm8AWgCVFdQXYnQamZVo51tcvmAqRjXn6q03m'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.get_user(screen_name = '@brendmm1')

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print("Status Received")
        text=clean(status.text)
        subject = text[0:3]
        msg = text
        send_email(subject,msg)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

# Define a function for the thread
def tweetListener (threadName):
    print("Running "+threadName+" thread")
    myStream.filter(follow=[str(user.id)])


thread1 = Thread( target = tweetListener, args = ("worker", ) )

print('Initialize')
print('Starting worker thread')
thread1.start()
while(True):
    time.sleep(5)
    if not myStream.running:
        print('Restarting worker thread')
        thread1.join()
        thread1.start()
