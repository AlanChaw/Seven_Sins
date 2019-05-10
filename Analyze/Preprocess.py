
# coding: utf-8

# # Analyse tweet data by districts and output result to couchdb

# ## load data from couchdb and initialise to py obj

# In[1]:

# sudo apt-get install python3-pip
# pip install nltk
# pip install --user couchdb

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys
import couchdb

server = couchdb.Server('http://admin:123456@localhost:5984/')
db = server['normal_sub_tweets']

analyse_type = sys.argv[1]
word_file_path = "./FindWords/" + analyse_type + "_words.txt"
print(word_file_path)


text_count = 0
all_record_list = []
for doc_id in db:
    text_count += 1
    suburb = db[doc_id]['suburb']
    text = db[doc_id]['doc']['doc']['text']
    all_record_list.append({
        "suburb": suburb,
        "text": text
    })


# ## Preprocess data with nltk
# Operations including tokenize twitter texts, lemmatize texts and load seed words


nltk.download('stopwords')
nltk.download('wordnet')

tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
lemmatizer = nltk.stem.WordNetLemmatizer()


def lemmatize(word):
    lemma = lemmatizer.lemmatize(word,'v')
    if lemma == word:
        lemma = lemmatizer.lemmatize(word,'n')
    return lemma

def pre_process(text) -> str:
    # lower cased
    text = text.lower()
    # tokenize
    words = tokenizer.tokenize(text)
    # check if word is alphabetic
    words = [w for w in words if w.isalpha()]
    # lemmatize
    words = [lemmatize(w) for w in words]
    # # remove stop words
    # stop_words = nltk.corpus.stopwords.words('english')
    # words = [w for w in words if not w in stop_words]
    # return result
    processed_comment = " ".join(words)
    return processed_comment


for record in all_record_list:
    text = record['text']
    processed_text = pre_process(text)
    record.update({
        "text": processed_text
    })



# ## load wordnet generated vocabularies and filter texts


related_words = []
with open(word_file_path, 'r') as f:
    words = f.readlines()
    for word in words:
        word = word.split()[0]
        word = lemmatize(word)
        related_words.append(word)


def containKeyword(text) -> bool:
    for word in related_words:
        if word in text:
#        print(word)
            return True
    return False


filterd_record_list = []
for record in all_record_list:
    if containKeyword(record['text']):
        record.update({
            "related": 1
        })
        filterd_record_list.append(record)


# ## Sentiment analysis by nltk vader sentiment analyser


nltk.download('vader_lexicon')

analyzer = SentimentIntensityAnalyzer()

for record in filterd_record_list:
    text = record['text']
    sentiment_results = analyzer.polarity_scores(text)
    neg_value = sentiment_results['neg']
    pos_value = sentiment_results['pos']
    if pos_value > neg_value:
        record.update({
            "sentiment": "pos"
        })
    elif pos_value < neg_value:
        record.update({
            "sentiment": "neg"
        })
    else:
        record.update({
            "sentiment": "neu"
        })


output_db_path = analyse_type + "_twitters"
try:
    processed_db = server.create(output_db_path)
except Exception as e:
    server.delete(output_db_path)
    processed_db = server.create(output_db_path)
processed_db.update(filterd_record_list)
