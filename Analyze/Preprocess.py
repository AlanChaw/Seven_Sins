
# coding: utf-8

# # Analyse tweet data by districts and output result to couchdb

# ## load data from couchdb and initialise to py obj

# In[1]:


import couchdb
# from collections import Counter

server = couchdb.Server('http://admin:123456@localhost:5984/')
db = server['total_jan_to_apr']

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

# suburb_text_dict = {}
# for doc_id in db:
#     suburb = db[doc_id]['suburb']
#     text = db[doc_id]['doc']['doc']['text']
#     if suburb not in suburb_text_dict.keys():
#         text_list = []
#         suburb_text_dict.update({
#             suburb: text_list
#         })
#     else:
#         text_list = suburb_text_dict.get(suburb)
#     text_list.append(text)

# suburb_info_list = []
# for suburb in suburb_text_dict.keys():
#     text_list = suburb_text_dict.get(suburb)
# #     print(suburb + ": " + str(len(text_list)))
#     suburb_info_list.append({
#         suburb: len(text_list)
#     })


# processed_db = server.create('processed_data')
# for suburb_info in suburb_info_list:
#     processed_db.save(suburb_info)



# ## Preprocess data with nltk
# Operations including tokenize twitter texts, lemmatize texts and load seed words

# In[2]:


import nltk
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
    # remove stop words
#     stop_words = nltk.corpus.stopwords.words('english')
#     words = [w for w in words if not w in stop_words]
    # return result
    processed_comment = " ".join(words)
    return processed_comment


for record in all_record_list:
    text = record['text']
    processed_text = pre_process(text)
    record.update({
        "text": processed_text
    })


# for key in suburb_text_dict.keys():
#     text_list = suburb_text_dict.get(key)
#     processed_text_list = []
#     for text in text_list:
#         processed_text_list.append(pre_process(text))
#     suburb_text_dict.update({
#         key: processed_text_list
#     })


# ## load wordnet generated vocabularies and filter texts

# In[3]:


food_words = []
with open("./FindWords/food_words.txt", 'r') as f:
    words = f.readlines()
    for word in words:
        word = word.split()[0]
        word = lemmatize(word)
        food_words.append(word)

def containKeyword(text) -> bool:
    for word in food_words:
        if word in text:
#             print(word)
            return True
    return False

for record in all_record_list:
    if containKeyword(record['text']):
        record.update({
            "related": 1
        })
    else:
        record.update({
            "related": 0
        })

# len(processed_record_list)

# for key in suburb_text_dict.keys():
#     text_list = suburb_text_dict[key]
#     processed_text_list = [text for text in text_list if containKeyword(text)]
#     suburb_text_dict.update({
#         key: processed_text_list
#     })


# ## Sentiment analysis by nltk vader sentiment analyser

# In[4]:


import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

analyzer = SentimentIntensityAnalyzer()

for record in all_record_list:
    if record['related'] == 0:
        record.update({
            "sentiment": "unrelated"
        })
        continue
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

# suburb_sentiment_dict = {}

# for key in suburb_text_dict.keys():
#     text_list = suburb_text_dict.get(key)
#     if key not in suburb_sentiment_dict:
#         sentiment_dict = {
#             'pos': 0,
#             'neg': 0,
#             'neu': 0,
#             'total': 0
#         }
#         suburb_sentiment_dict.update({
#             key: sentiment_dict
#         })
#     else:
#         sentiment_dict = suburb_sentiment_dict.get(key)

#     for text in text_list:
#         sentiment_results = analyzer.polarity_scores(text)
#         neg_value = sentiment_results['neg']
#         pos_value = sentiment_results['pos']
#         if pos_value > neg_value:
#             sentiment_dict['pos'] += 1
#         elif pos_value < neg_value:
#             sentiment_dict['neg'] += 1
#         else:
#             sentiment_dict['neu'] += 1
#     sentiment_dict['total'] = sentiment_dict['pos'] + sentiment_dict['neg'] + sentiment_dict['neu']
#     suburb_sentiment_dict.update({
#         key: sentiment_dict
#     })



# ## Check and Output analysed data to couchdb

# In[5]:



import re
import json

# boundaryJS = json.load(open('./origin_melb.json'))
# name_list=[]
# for ele in boundaryJS["features"]:
#     name_list.append(ele['properties']["SA2_NAME16"])


# def sub_name_normalisation(input_name):

#     for standard_sub in name_list:
#         if input_name.lower() == standard_sub.lower() or input_name.lower() in standard_sub.lower():
#             return standard_sub
#         if input_name.replace(" ", " - ").lower()==standard_sub.lower() or input_name.replace(" ", " - ").lower() in standard_sub.lower():
#             return standard_sub
#     for standard_sub in name_list:
#         if ('South' not in standard_sub) and ('North' not in standard_sub) and ('West' not in standard_sub) and ('East' not in standard_sub):
#             new = re.sub(r' South| North| West| East', '', input_name)
#             if new.lower() ==standard_sub.lower() or new.lower() in standard_sub.lower():
#                 return standard_sub
#     return None

# for record in all_record_list:
#     if record['related'] == 0:
#         continue
#     else:
#         nomalized_suburb = sub_name_normalisation(record['suburb'])
#         if nomalized_suburb is not None:
#             record.update({
#                 "suburb": nomalized_suburb
#             })

try:
    processed_db = server.create('analysed_twitters')
except Exception as e:
    server.delete('analysed_twitters')
    processed_db = server.create('analysed_twitters')
processed_db.update(all_record_list)
