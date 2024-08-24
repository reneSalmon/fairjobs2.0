import pandas as pd
import numpy as nm

import string
import unidecode
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def get_data(nrows=10000):
    """gets data"""
    df = pd.read_csv("../raw_data/data_full_df_web.csv", nrows=nrows)
    return df

def clean_text(text):
    """cleans and removes punctuations, number and stopwords from the text"""
    text_urless=re.sub(r"(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*", '', text)

    for punctuation in string.punctuation:
        text = text_urless.replace(punctuation, ' ') # Remove Punctuation

    lowercased = text.lower() # Lower Case

    unaccented_string = unidecode.unidecode(lowercased) # remove accents

    tokenized = word_tokenize(unaccented_string) # Tokenize

    words_only = [word for word in tokenized if word.isalpha()] # Remove numbers

    stop_words = set(stopwords.words('english')) # Make stopword list

    without_stopwords = [word for word in words_only if not word in stop_words] # Remove Stop Words

    return without_stopwords

def clean_df(df):

    df["clean_description"] = df["job_description"].apply(clean_text)

    return df

if __name__ == '__main__':
    df = get_data()
