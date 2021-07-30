import tweepy
from threading import Thread
import time
from tweepy.streaming import StreamListener
import smtplib
#Config file must be created to include api keys and email credentials
import config

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

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)

user = api.get_user(screen_name = '@mattswider')

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if (
            (not status.retweeted) and 
            ('RT @' not in status.text) and 
            (status.text[0:1] != '@')
        ):
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
    while True:
        try:
            myStream.filter(follow=[str(user.id)])
        except Exception as e:
            print("Exception caught:", e)
        print("Restarting "+threadName+" thread")


thread1 = Thread( target = tweetListener, args = ("worker", ) )

print('Initialize')
print('Starting worker thread')
thread1.start()
while(True):
    time.sleep(5)
    if not myStream.running:
        try:
            thread1.join()
            break
        except Exception as e:
            print("Exception caught when joining thread", e)  
