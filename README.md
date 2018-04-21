# Twitter Feel

The twitter feel script takes recent tweets on a chosen topic and calucluale how people feel about that specific subject using textblob library generate a csv file with all the data of the tweet , a table containing sentiment data and location in a html file 

## Getting Started

I havr built two versions of this script : tw_feel_wco.py and tw_feel.py

    tw_feel.py: this version uses colorama library for adding color to the text


    tw_feel_wco.py: this version is the same but without colorama styling

    
### Prerequisites

You will need this following libraries :

Tweepy :    pip install tweepy

Textblob :  pip install textblob

Pandas :    pip install pandas

OpenCV :    pip install opencv

Only if u want to run tw_feel.py 

Colorama :  pip install tweepy


### Usage

    python tw_feel.py

    python tw_feel_wco.py
    
 the script will ask for how many tweets u want to grab the limit is 100 the u chose your topic and lastly u chose the language   en=english,ar:arabic,fr=french the script will translate the tweets using the textblob translate(to='') function and he will give u a detailed csv file and a html file with all the data 
 

### Sample
i use CSVpad for viewing csv file :

![alt tag](https://github.com/alchemist107/twitter_feel/blob/master/csv.jpg)

html file :

![alt tag](https://github.com/alchemist107/twitter_feel/blob/master/html.jpg)



