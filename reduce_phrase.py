import spacy
from helper_tools import sanatize
import csv
from mapper import Mapper

nlp = spacy.load('en_core_web_lg')

def get_words_from_csv(filename):
    with open(filename, 'r') as f:
      reader = csv.reader(f)
      word_list = list(reader)
      word_list = [x[0] for x in word_list]
      return(word_list)

remove_list = get_words_from_csv('remove_list.csv')
stopwords = get_words_from_csv('stopwords.csv')

def reduce_to_noun_phrases(string):
    phrases = []
    doc = nlp(sanatize(string))
    for np in doc.noun_chunks:
        cleaned = ' '.join([x.lemma_ for x in np if x.lemma_ not in remove_list + stopwords])
        phrases.append(cleaned)
    return phrases

p = reduce_to_noun_phrases(string)

for phrase in p:
    m = Mapper(phrase)
    m.standard_search(show_scores = True)
    print(phrase)
    print(m.matches)
    print()
