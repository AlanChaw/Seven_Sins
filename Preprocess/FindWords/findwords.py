
from nltk.corpus import wordnet as wn

seedWords = []
with open("./food_seeds.txt", 'r') as f:
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

with open("food_words.txt", 'w') as f:
    for word in finalWords:
        f.write(word + "\n")
