import random
#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np
from nltk.stem import PorterStemmer
import spacy
import time

nlp = spacy.load('en_core_web_sm')
stemmer = PorterStemmer()
stop_words = nlp.Defaults.stop_words


def preprocess_text(text):
    doc = nlp(text)
    preprocessed_tokens = [
        token.lemma_ for token in doc if token.text.lower() not in stop_words
        ]
    return " ".join([stemmer.stem(token) for token in preprocessed_tokens])


# In[5]:


import pandas as pd
import numpy as np
import string
# FRE SCORE
from textstat import flesch_reading_ease
# SENTIMENT ANALYSIS USING VADER
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#POS TAGGING
import spacy
#VECTORISING TEXT AND CREATING PIPELINE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
#COSINE SIMILARITY BETWEEN REVIEWS
from sklearn.metrics.pairwise import cosine_similarity


# In[6]:


df = pd.read_csv("WELFake_Dataset.csv")


# In[7]:


df.columns


# In[8]:


#RENAME COLUMNS
df.rename(columns={'text': 'NEWS TEXT'}, inplace=True)
df.rename(columns={'title': 'NEWS TITLE'}, inplace=True)
df.rename(columns={'label': 'LABEL'}, inplace=True)


# In[9]:


# df['PREPROCESSED TEXT'] = df['NEWS TEXT'].apply(preprocess_text)


# In[10]:


def add_readability_score(df):
    df['READABILITY_FRE'] = df['NEWS TEXT'].apply(
        lambda d: flesch_reading_ease(d))

def add_title_length(df):
    df['TITLE_LENGTH'] = df['NEWS TITLE'].apply(lambda d: len(d))

def add_text_length(df):
    df['TEXT LENGTH'] = df['NEWS TEXT'].apply(lambda d: len(d))

def add_vader_text_sentiment_score(df):
    sid = SentimentIntensityAnalyzer()

    df['TEXT SENTIMENT SCORE'] = df['NEWS TEXT'].apply(
        lambda d: sid.polarity_scores(d)['compound'])
    
def add_vader_title_sentiment_score(df):
    sid = SentimentIntensityAnalyzer()

    df['TITLE SENTIMENT SCORE'] = df['NEWS TITLE'].apply(
        lambda d: sid.polarity_scores(d)['compound'])
    
def add_sentiment_category(df, threshold):

    def assign_sentiment_category(score):
        if score > threshold:
            return 1
        else:
            return 0

    df['SENTIMENT CATEGORY'] = df['TEXT SENTIMENT SCORE'].apply(
        assign_sentiment_category)
    
def add_count_punctuation(df):
    def count_punctuation(text):
        punctuation_count = sum([1 for char in text if char in string.punctuation])
        return punctuation_count
    
    # Assuming you have a DataFrame called 'df' with a column 'REVIEW_TEXT'
    df['TEXT PUNCTUATION COUNT'] = df['NEWS TEXT'].apply(count_punctuation)

def add_count_capital_chars(df):
    def count_capital_chars(text):
        capital_count = sum([1 for char in text if char.isupper()])
        return capital_count


    # Assuming you have a DataFrame called 'df' with a column 'REVIEW_TEXT'
    df['TEXT CAPITAL CHARS'] = df['NEWS TEXT'].apply(count_capital_chars)

def add_pos_tags(df):
    def count_pos(Pos_counts, pos_type):
        pos_count = Pos_counts.get(pos_type, 0)
        return pos_count

    def pos_counts(text):
        doc = nlp(text)
        Pos_counts = doc.count_by(spacy.attrs.POS)
        return Pos_counts

    poscounts =  df["NEWS TEXT"].apply(pos_counts)
    df['TEXT NUM NOUNS'] = df['NEWS TEXT'].apply(
        lambda text: count_pos(poscounts, spacy.parts_of_speech.NOUN))
    df['TEXT NUM VERBS'] = df['NEWS TEXT'].apply(
        lambda text: count_pos(poscounts, spacy.parts_of_speech.VERB))
    df['TEXT NUM ADJECTIVES'] = df['NEWS TEXT'].apply(
        lambda text: count_pos(poscounts, spacy.parts_of_speech.ADJ))
    df['TEXT NUM ADVERBS'] = df['NEWS TEXT'].apply(
        lambda text: count_pos(poscounts, spacy.parts_of_speech.ADV))
    
def add_named_entities(df):
    def count_entities(text):
        doc = nlp(text)
        ent_count = len([ent.text for ent in doc.ents])
        return ent_count

    df['TEXT NUM NAMED ENTITIES'] = df['NEWS TEXT'].apply(count_entities)
    
def calculate_lexical_diversity(text):
    words = text.split()
    total_words = len(words)
    unique_words = len(set(words))
    
    if total_words > 0:
        lexical_diversity = unique_words / total_words
    else:
        lexical_diversity = 0.0
    
    return lexical_diversity


# In[11]:


df.isnull().sum()


# In[12]:


#REMOVE NULL RECORDS
df = df.dropna()


# In[13]:


#USE ONLY 20,000 RECORDS
df1 = df[:20000]


# In[14]:


#ADD COLUMN FOR NUMBER OF WORDS IN TEXT
df1['TEXT WORD COUNT'] = df1['NEWS TEXT'].apply(lambda x: len(x.split()))


# In[15]:


#ADD COLUMN FOR NUMBER OF WORDS IN TITLE
df1["TITLE WORD COUNT"] = df1["NEWS TITLE"].apply(lambda x: len(x.split()))


# In[16]:


#ADD TEXT LENGTH AND TITLE LENGTH
add_text_length(df1)
add_title_length(df1)


# In[17]:


#ADD SENTIMENT SCORE OF TEXT
add_vader_text_sentiment_score(df1)


# In[18]:


df1.columns


# In[19]:


#ADD VADER SENTIMENT SCORE OF TITLE
add_vader_title_sentiment_score(df1)


# In[20]:


#ADD READABILITY SCORE OF TEXT
add_readability_score(df1)


# In[21]:


#ADD CAPITAL CHARACTER COUNT
add_count_capital_chars(df1)


# In[22]:


#ADD PUNCTUATION COUNT
add_count_punctuation(df1)


# In[23]:


def add_pos_tags(df):
    def count_pos(Pos_counts, pos_type):
        pos_count = Pos_counts.get(pos_type, 0)
        return pos_count

    def pos_counts(text):
        doc = nlp(text)
        Pos_counts = doc.count_by(spacy.attrs.POS)
        return Pos_counts

    poscounts =  df["NEWS TEXT"].apply(pos_counts)
    df['TEXT NUM NOUNS'] = df['NEWS TEXT'].apply(
        lambda text: count_pos(poscounts, spacy.parts_of_speech.NOUN))
    df['TEXT NUM VERBS'] = df['NEWS TEXT'].apply(
        lambda text: count_pos(poscounts, spacy.parts_of_speech.VERB))
    df['TEXT NUM ADJECTIVES'] = df['NEWS TEXT'].apply(
        lambda text: count_pos(poscounts, spacy.parts_of_speech.ADJ))
    df['TEXT NUM ADVERBS'] = df['NEWS TEXT'].apply(
        lambda text: count_pos(poscounts, spacy.parts_of_speech.ADV))


# In[24]:


#ADD POS TAGS
add_pos_tags(df1)


# In[ ]:


df2 = df1[:10000]


# In[ ]:


#ADD COUNT OF NAMES ENTITIES IN TEXT
add_named_entities(df2)


# In[ ]:


#ADD SENTIMENT CATEGORY OF TEXT
add_sentiment_category(df1)


# In[27]:


#SAVE AS CSV FILE

df1.to_csv("training_data_set_1.csv")


# In[26]:


#ADD LEXICAL DIVERSITY
df['TEXT LEXICAL DIVERSITY'] = df['NEWS TEXT'].apply(calculate_lexical_diversity)


# In[28]:


#TRAIN MODELS
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, f1_score, roc_auc_score, precision_score, recall_score, classification_report
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import LinearSVC, SVC
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.linear_model import RidgeClassifier, SGDClassifier, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer


# In[29]:


classifiers = {}
classifiers.update({"XGBClassifier": XGBClassifier(eval_metric='logloss',objective='binary:logistic',use_label_encoder=False)})
# classifiers.update({"CatBoostClassifier": CatBoostClassifier(silent=True)})
classifiers.update({"LinearSVC": LinearSVC(max_iter=10000)})
# classifiers.update({"MultinomialNB": MultinomialNB()})
# classifiers.update({"LGBMClassifier": LGBMClassifier()})
classifiers.update({"RandomForestClassifier": RandomForestClassifier()})
classifiers.update({"DecisionTreeClassifier": DecisionTreeClassifier()})
classifiers.update({"ExtraTreeClassifier": ExtraTreeClassifier()})
classifiers.update({"AdaBoostClassifier": AdaBoostClassifier()})
classifiers.update({"KNeighborsClassifier": KNeighborsClassifier()})
classifiers.update({"RidgeClassifier": RidgeClassifier()})
classifiers.update({"SGDClassifier": SGDClassifier()})
classifiers.update({"BaggingClassifier": BaggingClassifier()})
classifiers.update({"BernoulliNB": BernoulliNB()})
classifiers.update({"LogisticRegression": LogisticRegression()})
classifiers.update({"SVM": SVC()})


# In[ ]:


df1.columns


# In[30]:


features_numeric = [
    'TEXT WORD COUNT', 'TITLE WORD COUNT', 'TEXT LENGTH', 'TITLE_LENGTH',
       'TEXT SENTIMENT SCORE', 'TITLE SENTIMENT SCORE', 'READABILITY_FRE',
       'TEXT CAPITAL CHARS', 'TEXT PUNCTUATION COUNT']


# In[31]:


X = df1[features_numeric]
Y = df1["LABEL"]


# In[32]:


X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42)


# In[33]:


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# In[34]:


# CREATE A DATAFRAME OF MODELS WITH RUN TIME AND AUC SCORES



with open("moedl_1.pkl", "rb") as file:
    model = file["MODEL"]
    scaler = file["SCALER"]
def get_score(ipfs_address):
    # Generate a random double value between 0 and 1
    return random.random(0,1)
