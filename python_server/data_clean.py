import pandas as pd
import numpy as np
import re
import string
from ast import literal_eval
from sklearn import preprocessing
from preprocessor import api as p
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

punc = string.punctuation
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
def remove_stop_words(text):
    return " ".join([word for word in str(text).split() if word not in stop_words])

def removeNumbers(text):
    """ Removes integers """
    text = ''.join([i for i in text if not i.isdigit()])         
    return text

def remove_punc(text):
    """custom function to remove the frequent words"""
    return " ".join([word for word in str(text).split() if word not in punc])

def lemmatize_text(text):
    return " ".join([lemmatizer.lemmatize(w) for w in word_tokenize(text)])

def stem_text(text):
    return " ".join([stemmer.stem(w) for w in word_tokenize(text)])

def f(x):
    try:
        return literal_eval(str(x))   
    except Exception as e:
        #print(x, e)
        return []
    
def remove_spaces(text):
    return " ".join([word for word in str(text).split()])

def listit(x):
    try: 
        return x.split(',')
    except:
        return np.nan
    
def delinklistit(x):
    try: 
        op=[]
        a= x.split(',')
        for i in a:
            op.append(i.split('/')[-1])
        return op
    except:
        return np.nan
    
def dedup(l):
    ul=[]
    try:
        for i in l:
            if i not in ul:
                ul.append(i)
        return ul
    except:
        return np.nan

def stringit(x):
    st=""
    try:
        for i in x:
            st= st+', '+i
    except:
        pass
    return st

df= pd.read_csv('../data/video_metadata.csv')
df['video_tags']= df['video_tags'].apply(lambda x: listit(x))
df['video_topics']=df['video_topics'].apply(lambda x: delinklistit(x))
df['video_title']= df['video_title'].astype('str')
df['video_title']= df['video_title'].str.lower()
df['video_title']= df['video_title'].str.strip()
df['video_title'] = df['video_title'].apply(lambda text: removeNumbers(text))
df['video_title'] = df['video_title'].apply(lambda text: remove_punc(text))
df["video_title"] = df['video_title'].str.replace('[^\w\s]','')
df['video_title'] = df['video_title'].apply(lambda text: remove_stop_words(text))
df['video_title'] = df['video_title'].str.strip()
df['video_title'] = df['video_title'].apply(lambda text: remove_spaces(text))

a= df.groupby('channel_id')['video_title'].agg(lambda x: " ".join(x)).reset_index()
b= df.groupby('channel_id')[['video_tags', 'video_topics']].agg('sum').reset_index()
df= pd.merge(a, b)
df['video_topics']= df['video_topics'].apply(lambda x: dedup(x))
df['video_tags']= df['video_tags'].apply(lambda x: stringit(x))
df['video_topics']= df['video_topics'].apply(lambda x: stringit(x))

df1= pd.read_csv('../data/subscribed_channels.csv')
df= pd.merge(df, df1)
df= df[['channel_id', 'channel_title', 'channel_descr', 'video_title', 'video_tags', 'video_topics']]
df['channel_descr']= df['channel_descr'].str.lower()
df['channel_descr']= df['channel_descr'].astype('str')
df['channel_descr']= df['channel_descr'].str.strip()
df['channel_descr']= df['channel_descr'].str.strip()
df['channel_descr'] = df['channel_descr'].apply(lambda text: removeNumbers(text))
df['channel_descr'] = df['channel_descr'].apply(lambda text: remove_punc(text))
df["channel_descr"] = df['channel_descr'].str.replace('[^\w\s]','')
df['channel_descr'] = df['channel_descr'].apply(lambda text: remove_stop_words(text))
df['channel_descr'] = df['channel_descr'].str.strip()
df['channel_descr'] = df['channel_descr'].apply(lambda text: remove_spaces(text))
df['corpus_text']= df['channel_descr']+' '+ df['video_title']+ ' '+df['video_tags']+ ' '+df['video_topics']

df[['channel_id', 'channel_title', 'video_topics', 'corpus_text']].to_csv('../data/final_data.csv', index=False)
