
from nltk.corpus import wordnet as wn
import sys
from nltk.corpus import stopwords

seed_words_name = sys.argv[1]

seed_words_file = seed_words_name + "_seeds.txt"

seedWords = []
with open(seed_words_file, 'r') as f:
    words = f.readlines()
    for word in words:
        word = word.split()[0]
        seedWords.append(word)

finalWords = set()

for seed in seedWords:
    for synset in wn.synsets(seed):
        for lemma in synset.lemmas():
            finalWords.add(lemma.name())
            # print(lemma.name())

stop_words = stopwords.words('english')
final_words = [w for w in finalWords if w not in stop_words]


output_words_file = seed_words_name + "_words.txt"
with open(output_words_file, 'w') as f:
    for word in final_words:
        f.write(word + "\n")
