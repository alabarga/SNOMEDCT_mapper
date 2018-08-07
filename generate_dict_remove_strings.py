from nltk.corpus import words
from read_snomed import load_lexicon
from helper_tools import sanatize, remove_words
from tqdm import tqdm
import csv

import spacy
nlp = spacy.load('en_core_web_lg')

def get_lemma(word):
    if len(word.split()) != 1:
        raise ValueError('Only input >>>single<<< words')
    doc = nlp(word)
    lemma = doc[0].lemma_
    return(lemma)

recommended = load_lexicon('recommended')

# Get NLTK corpus
print('Lemmatizing NLTK')
words = words.words()
lemmas = [get_lemma(word) for word in tqdm(words, desc = 'NLTK lemmas')]
lemmas = set(lemmas)

print('Lemmatizing SNOMED')
recommended_lemmas = []
for syn in tqdm(recommended, desc = 'SNOMED CT lemmas'):
    doc = nlp(syn.term)
    for token in doc:
        recommended_lemmas.append(token.lemma_)

recommended_lemmas = set(recommended_lemmas)

remove_list = list(lemmas - recommended_lemmas)

with open("dict_strings.csv",'w', newline='') as resultFile:
    wr = csv.writer(resultFile)
    for lemma in sorted(remove_list):
        wr.writerow([lemma])
