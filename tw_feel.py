import tweepy
from textblob import TextBlob
import sys
import os
import csv
import io
import pandas as pd
import re
import colorama
from colorama import Fore, Back, Style

colorama.init()

#banner rendred using "http://patorjk.com/software/taag/#p=display&f=3D%20Diagonal&t=twitter-feel"

banner = ("""

                                                                                                                       
                                                                                                                       
    ___                             ___      ___                                                               ,--,    
  ,--.'|_                  ,--,   ,--.'|_  ,--.'|_                                 .--.,                     ,--.'|    
  |  | :,'          .---.,--.'|   |  | :,' |  | :,'             __  ,-.    ,---,.,--.'  \                    |  | :    
  :  : ' :         /. ./||  |,    :  : ' : :  : ' :           ,' ,'/ /|  ,'  .' ||  | /\/                    :  : '    
.;__,'  /       .-'-. ' |`--'_  .;__,'  /.;__,'  /     ,---.  '  | |' |,---.'   ,:  : :     ,---.     ,---.  |  ' |    
|  |   |       /___/ \: |,' ,'| |  |   | |  |   |     /     \ |  |   ,'|   |    |:  | |-,  /     \   /     \ '  | |    
:__,'| :    .-'.. '   ' .'  | | :__,'| : :__,'| :    /    /  |'  :  /  :   :  .' |  : :/| /    /  | /    /  ||  | :    
  '  : |__ /___/ \:     '|  | :   '  : |__ '  : |__ .    ' / ||  | '   :   |.'   |  |  .'.    ' / |.    ' / |'  : |__  
  |  | '.'|.   \  ' .\   '  : |__ |  | '.'||  | '.'|'   ;   /|;  : |   `---'     '  : '  '   ;   /|'   ;   /||  | '.'| 
  ;  :    ; \   \   ' \ ||  | '.'|;  :    ;;  :    ;'   |  / ||  , ;             |  | |  '   |  / |'   |  / |;  :    ; 
  |  ,   /   \   \  |--" ;  :    ;|  ,   / |  ,   / |   :    | ---'              |  : \  |   :    ||   :    ||  ,   /  
   ---`-'     \   \ |    |  ,   /  ---`-'   ---`-'   \   \  /                    |  |,'   \   \  /  \   \  /  ---`-'   
               '---"      ---`-'                      `----'                     `--'      `----'    `----'            
                                                                                                                       

                                                                                                                      

/Twitter-Feel Script Developed in Python 3.6
/Developed By Chamsddine Bouzaine
""")

print (Fore.MAGENTA + banner)
print(Style.RESET_ALL)

#gettening variable for authentication

consumer_key = 'consumer_key HERE !'
consumer_secret = 'consumer_secret HERE !'

access_token = 'access_token HERE !'
access_token_secret = 'access_token_secret HERE !'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)


#grab subject to analyse
tweetPerQry = input ( 'how many tweets do u want to grab (1-100) : ')
subject = input ('chose a subject to search for its sentiment:  ')
lang = input ("chose the language of the tweets  : Ar=arabic, Fr=french, En=english  ")
public_tweets = api.search(q=subject, count=tweetPerQry, lang=lang)

filename = subject +"_feel.csv"  #creating filename based on subject

#grab data and write to csv file

with open(filename,'w', encoding= "utf-8") as csvfile:
    fieldnames = ['Name', 'Twitter Handle', 'Favourites_Count', 'Followers', 'User_Id','User_Verified','User Location',
                 'Date of Tweet', 'Tweet Id', 'Tweet Text', 'Language', 'Tweet Source', 'Tweet Retweet', 'Tweet Reply To Id',
                 'Reply To Name','polarity','subjectivity']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    polarity = 0
    for tweet in public_tweets:
        row = {}
        row['Name'] = str(tweet.user.name)
        row['Tweet Text'] = str(tweet.text)
        row['Twitter Handle'] = str(tweet.user.screen_name)
        row['Favourites_Count'] = str(tweet.user.favourites_count)
        row['Followers'] = str(tweet.user.followers_count)
        row['User_Id'] = str(tweet.user.id)
        row['User_Verified'] = str(tweet.user.verified)
        row['User Location'] = str(tweet.user.location)
        row['Date of Tweet'] = str(tweet.user.created_at)
        row['Tweet Id'] = str(tweet.id)
        row['Language'] = str(tweet.lang)
        row['Tweet Source'] = str(tweet.source)
        row['Tweet Retweet'] = str(tweet.retweet_count)
        row['Tweet Reply To Id'] = str(tweet.in_reply_to_user_id)
        row['Reply To Name'] = str(tweet.in_reply_to_screen_name)
        analysis = TextBlob(tweet.text)
        language = analysis.detect_language() #detect language of tweet to tweak the encoder 

        #translate the text so we can get the sentiment
        if language == 'en':
            row ['polarity'] = (analysis.sentiment.polarity)
            row ['subjectivity'] = (analysis.sentiment.subjectivity)    
            polarity = polarity + (analysis.sentiment.polarity)
        else:
            translated = analysis.translate(to='en')
            row ['polarity'] = (translated.sentiment.polarity)
            row ['subjectivity'] = (translated.sentiment.subjectivity)
            polarity = polarity + (translated.sentiment.polarity)

    
        print(Fore.GREEN + str(polarity) + Style.RESET_ALL)

        tweet = len(public_tweets) #calculate how many tweets:
        writer.writerow(row) #write data to csv

        print (Fore.MAGENTA + analysis.detect_language() + Style.RESET_ALL)

print (Fore.RED + str(tweet) + Style.RESET_ALL , "tweets found , the data have been written to ", filename)
print ("opinion score = " ,polarity)
if polarity >= 0:
    print(Fore.GREEN + "the people think positivly about this subject" + Style.RESET_ALL)
else:
    print (Fore.MAGENTA + "the people think negativly about this subject" + Style.RESET_ALL)

#creating a html table 
#changing encoder with specific language u can tweak it as u like  
if lang == 'en':
    df = pd.read_csv(filename, encoding='ANSI')
    df.to_html( subject + 'feel.html', columns=['Twitter Handle','User Location','polarity','subjectivity'] )
    print ('a html table has been created to this file :' ,subject ,'_feel.html')


elif lang == 'fr':
    df = pd.read_csv(filename, encoding='ANSI')
    df.to_html( subject + 'feel.html' , columns=['Twitter Handle','User Location','polarity','subjectivity'])
    print ('a html table has been created to this file :' ,subject ,'_feel.html')
    
else:
    df = pd.read_csv(filename, encoding='utf-8')
    df.to_html( 'ar_feel.html' , columns=['Twitter Handle','User Location','polarity','subjectivity'])
    print ('a html table has been created to this file :' ,subject ,'_feel.html')


