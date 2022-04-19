
import nltk
from regex import P
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from glob import escape
from itertools import count
from math import degrees
from operator import methodcaller
import re
from flask import Flask,render_template, request
#from get0 import temp_function
app = Flask(__name__ , template_folder='template')

#---------------------------------------------------

from operator import mod
import tweepy
import configparser
import pandas as pd

# read configs
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# User

limit = 1
#---------------------------------------------------

import string
from collections import Counter

#import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
nltk.download('vader_lexicon')

#---------------------------------

#--------------------------------
@app.route ('/')
def start():
      return render_template('index.html')

#---

@app.route('/result', methods =["GET", "POST"])

def hello():
     if request.method == "POST":
            name = request.form.get('username')
            #print(name)
            tweets = api.user_timeline(screen_name = name , count = limit , tweet_mode='extended')
            #for t in range (0,5):
                  #tweet = tweets[t].full_text
            strr = tweets[0].full_text
            print(strr)
            # print("-------------------------------")
            
            #------------NLP-------------- #
            text=strr
            lower_case = text.lower()
            cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
            # Using word_tokenize because it's faster than split()
            tokenized_words = word_tokenize(cleaned_text, "english")	
            # Removing Stop Words
            final_words = []
            for word in tokenized_words:
                if word not in stopwords.words('english'):
                    final_words.append(word)

            # Lemmatization - From plural to single + Base form of a word (example better-> good)
            lemma_words = []
            for word in final_words:
                word = WordNetLemmatizer().lemmatize(word)
                lemma_words.append(word)

            emotion_list = []
            with open('emotion.txt', 'r') as file:
                for line in file:
                    clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
                    word, emotion = clear_line.split(':')

                    if word in lemma_words:
                        emotion_list.append(emotion)

            #print(emotion_list)
            w = Counter(emotion_list)
            #print(w)

            out = ''
            def sentiment_analyse(sentiment_text):
                score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
                if score['neg'] > score['pos']:
                    #out="Negative Sentiment"
                    out='Please click on quentionaire page'
                    return (out)  
                elif score['neg'] < score['pos']:
                    #out="Positive Sentiment"
                    out ='You seem alright ...Thank you'
                    return (out)  
                else:
                    #out="Neutral Sentiment"
                    out ='You seem alright ...Thank you'
                    return (out)  
                 

            out = sentiment_analyse(cleaned_text)
            return render_template('first.html',name = name, tweets= tweets , out = out )



@app.route('/q1.html')
def question():
      return render_template('q1.html')

if __name__ == '__main__':
    ##app.debug = True
    app.run(debug=True)