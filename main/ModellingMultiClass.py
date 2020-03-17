import pandas as pd
import numpy as np
import os
import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from collections import defaultdict
#from sklearn.preprocessing import MultiLabelBinarizer
#from sklearn.model_selection import train_test_split
#from sklearn.metrics import confusion_matrix
#from sklearn.metrics import classification_report
from keras.models import load_model
from collections import Counter
import itertools
import retweet_maker

def clean_str(string):
    string = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '',string)
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

def build_vocab(sentences):
    # Build vocabulary
    word_counts = Counter(itertools.chain(*sentences))
    # Mapping from index to word
    vocabulary_inv = [x[0] for x in word_counts.most_common()]
    # Mapping from word to index
    vocabulary = {x: i for i, x in enumerate(vocabulary_inv)}
    return [vocabulary, vocabulary_inv]


def preprocessing(flood_tweets):
	text1 = flood_tweets['Text'][0]
	string = clean_str(text1)


	cleaned_tweets = []
	for index, row in flood_tweets.iterrows():
		text = row['Text']
		text = clean_str(text)
		cleaned_tweets.append(text)
	flood_tweets['cleaned_text'] = cleaned_tweets


	texts = flood_tweets["cleaned_text"].values

	sequence_length = max(len(x.split()) for x in texts)

	x_text = [s.strip() for s in texts]
	x_text = [clean_str(sent) for sent in x_text]
	x_text = [s.split(" ") for s in x_text]

	vocabulary, vocabulary_inv = build_vocab(x_text)

	MAX_NUM_WORDS=1000 # how many unique words to use (i.e num rows in embedding vector)
	MAX_SEQUENCE_LENGTH=34 # max number of words in a review to use


	tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
	tokenizer.fit_on_texts(texts)
	sequences = tokenizer.texts_to_sequences(texts)

	word_index = tokenizer.word_index
	#print('Found %s unique tokens.' % len(word_index))
	data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

	return data


def modelling(data, flood_tweets):
	new_model = load_model('model_flood')
	prediction = new_model.predict(data)

	need_tweets_id = []
	supply_tweets_id = []
	for each in range(prediction.shape[0]):
	    if prediction[each][0] > 0.8:
	        supply_tweets_id.append(flood_tweets['Id'][each])
	    if prediction[each][1] > 0.8:
	        need_tweets_id.append(flood_tweets['Id'][each])

	return need_tweets_id, supply_tweets_id


def classify():
	flood_tweets = pd.read_csv("/home/shamik/KeralaFloods/test/collection.csv", header = 0)
	print(flood_tweets.shape)


	need_tweets_id = []
	supply_tweets_id = []

	data = preprocessing(flood_tweets)
	need_tweets_id, supply_tweets_id = modelling(data, flood_tweets)
	return need_tweets_id, supply_tweets_id

print("Modelling MC file")
need_list_id, supply_list_id = classify()
print("Calssification Done")
retweet_maker.retweet(supply_list_id)
print("supply" + str(supply_list_id))
retweet_maker.retweet(need_list_id)
print("need" + str(need_list_id))
print("Posted in Twitter")
