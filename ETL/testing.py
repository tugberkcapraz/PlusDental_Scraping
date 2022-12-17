# import data science libraries
import pandas as pd
import numpy as np#
import argparse
import json
import time
import numpy as np


# read csv file from the relative data directiory
reviews = pd.read_csv("../data/pd_rev_en.csv")

# print(reviews.head())
#print the first 5 rows of the dataframe
print(reviews.head())

# drop unnamed columns
reviews.drop(columns=['Unnamed: 0'], inplace=True)

# check if dropping worked
print(reviews.head())

#check shape of the dataframe
print(reviews.shape)

# drop duplicates
reviews.drop_duplicates(subset=['text'], keep='first', inplace=True)

#check shape of the dataframe
print(reviews.shape)


# write a function to split date columns into separate columns and save it into the same dataframe
def split_date(date):
    date = pd.to_datetime(date)
    return date.year, date.month, date.day
reviews['year'], reviews['month'], reviews['day'] = zip(*reviews['date'].apply(split_date))

print(reviews.head())

# write a functions to clean text column of the reviews dataframe for the NLP analysis
def clean_text(text):
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('\xa0', ' ')
    text = text.replace('\u200b', ' ')
    text = text.replace('\u200c', ' ')
    text = text.replace('\u200d', ' ')
    text = text.replace('\u200e', ' ')
    text = text.replace('\u200f', ' ')
    text = text.replace('\u202a', ' ')
    return text

# apply the function to the text column and save it as cleaned_text
reviews['cleaned_text'] = reviews['text'].apply(clean_text)
#check if working
print(reviews.cleaned_text.sample(10))


# write a function to remove stopwords from the text column
def remove_stopwords(text):
    from nltk.corpus import stopwords
    stopwords = stopwords.words('english')
    text = [word for word in text.split() if word not in stopwords]
    return ' '.join(text)

#apply the function to the cleaned_text column and save it as cleaned_text
reviews['cleaned_text'] = reviews['cleaned_text'].apply(remove_stopwords)
#check if working
print(reviews.cleaned_text.sample(10))

# write a function to remove punctuation from the text column
def remove_punctuation(text):

    """
    Remove punctuation from text.
    :param text:
    :return:
    """
    text = text.replace('.', '')
    text = text.replace(',', '')
    text = text.replace('!', '')
    text = text.replace('?', '')
    return text

#apply the function to the cleaned_text column and save it as cleaned_text
reviews['cleaned_text'] = reviews['cleaned_text'].apply(remove_punctuation)
#check if working
print(reviews.cleaned_text.sample(10))

# write a function to lemmatize the text column
def lemmatize_text(text):
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    text = [lemmatizer.lemmatize(word) for word in text.split()]
    return ' '.join(text)

# apply the function to the cleaned_text column and save it as cleaned_text
reviews['cleaned_text'] = reviews['cleaned_text'].apply(lemmatize_text)
#check if working
print(reviews.cleaned_text.sample(10))

# lowercase the text column
reviews['cleaned_text'] = reviews['cleaned_text'].apply(lambda x: x.lower())
#check if working
print(reviews.cleaned_text.sample(10))


# write a function which detects the verbs from a text
def detect_verbs(text):
    from nltk.tokenize import word_tokenize
    from nltk.corpus import wordnet
    from nltk.stem import WordNetLemmatizer
    from nltk.stem import PorterStemmer
    # stop importing and write the fucking function
    # tokenize the text
    tokens = word_tokenize(text)
    # lemmatize the text
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # stem the text
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]
    # find the verbs in the text
    verbs = [token for token in stemmed_tokens if wordnet.synsets(token, pos=wordnet.VERB)]
    return verbs

# apply it to the cleaned_text column
reviews['verbs'] = reviews['cleaned_text'].apply(detect_verbs)

# check if working
print(reviews.verbs.sample(10))

# filter the dataframe where there are 1 stars and pool all the verbs in a list
verbs_1 = reviews[reviews['stars'] == 1]['verbs'].apply(lambda x: x).tolist()
# check if working
print(verbs_1)

# flatten the nested list of verbs_1
verbs_1 = [item for sublist in verbs_1 for item in sublist]
# check if working
print(verbs_1)

# check the most common verbs in the verbs_1 list
print(pd.Series(verbs_1).value_counts())
