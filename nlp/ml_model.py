
from nltk.sentiment import SentimentIntensityAnalyzer
import os
import pandas as pd
from nltk.stem import PorterStemmer
import spacy
import string
from textstat import flesch_reading_ease
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
import pickle
import nltk
import streamlit as st
nlp = None
stemmer = None
stop_words = None
sid = None
model = None
scaler = None


def preprocess_text(text):
    doc = nlp(text)
    preprocessed_tokens = [
        token.lemma_ for token in doc if token.text.lower() not in stop_words
    ]
    return " ".join([stemmer.stem(token) for token in preprocessed_tokens])


def add_readability_score(df):
    df['READABILITY_FRE'] = df['NEWS TEXT'].apply(
        lambda d: flesch_reading_ease(d))


def add_title_length(df):
    df['TITLE_LENGTH'] = df['NEWS TITLE'].apply(lambda d: len(d))


def add_text_length(df):
    df['TEXT LENGTH'] = df['NEWS TEXT'].apply(lambda d: len(d))


def add_vader_text_sentiment_score(df):

    df['TEXT SENTIMENT SCORE'] = df['NEWS TEXT'].apply(
        lambda d: sid.polarity_scores(d)['compound'])


def add_vader_title_sentiment_score(df):

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
        punctuation_count = sum(
            [1 for char in text if char in string.punctuation])
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

    poscounts = df["NEWS TEXT"].apply(pos_counts)
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


def get_score(content):
    global nlp, stemmer, stop_words, sid, model, scaler

    nlp = spacy.load('en_core_web_sm')
    stemmer = PorterStemmer()
    stop_words = nlp.Defaults.stop_words
    sid = SentimentIntensityAnalyzer()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    model_file_path = os.path.join(current_dir, "model_1.pkl")
    with open(model_file_path, "rb") as file:
        data = pickle.load(file)
        
    model = data["MODEL"]
    scaler = data["SCALER"]

    data = {
        'NEWS TITLE': [content.split("\n")[0]],
        'NEWS TEXT': [" ".join(content.split("\n")[1:])]
    }

    df1 = pd.DataFrame(data)

    # NEWS TEXT WORD COUNT
    df1['TEXT WORD COUNT'] = df1['NEWS TEXT'].apply(lambda x: len(x.split()))

    # ADD COLUMN FOR NUMBER OF WORDS IN TITLE
    df1["TITLE WORD COUNT"] = df1["NEWS TITLE"].apply(lambda x: len(x.split()))

    # ADD TEXT LENGTH AND TITLE LENGTH
    add_text_length(df1)
    add_title_length(df1)
    # ADD SENTIMENT SCORE OF TEXT
    add_vader_text_sentiment_score(df1)
    # ADD VADER SENTIMENT SCORE OF TITLE
    add_vader_title_sentiment_score(df1)
    # ADD READABILITY SCORE OF TEXT
    add_readability_score(df1)
    # ADD CAPITAL CHARACTER COUNT
    add_count_capital_chars(df1)
    # ADD PUNCTUATION COUNT
    add_count_punctuation(df1)

    # ADD LEXICAL DIVERSITY
    df1['TEXT LEXICAL DIVERSITY'] = df1['NEWS TEXT'].apply(
        calculate_lexical_diversity)

    features_numeric = [
        'TEXT WORD COUNT', 'TITLE WORD COUNT', 'TEXT LENGTH', 'TITLE_LENGTH',
        'TEXT SENTIMENT SCORE', 'TITLE SENTIMENT SCORE', 'READABILITY_FRE',
        'TEXT CAPITAL CHARS', 'TEXT PUNCTUATION COUNT']

    X = df1[features_numeric]
    X_scaled = scaler.transform(X)
    prediction = model.predict_proba(X_scaled)
    return prediction[:, 1][0]
