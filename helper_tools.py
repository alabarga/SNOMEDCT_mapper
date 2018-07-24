# A collection of helpful tools I tend to need in these scripts
import collections

def group(lst, n):
    # Group items in a list into tuples of size 'n'
    return zip(*[lst[i::n] for i in range(n)])

def flatten(l):
# Flattens any nested list - even irregular ones
# See here: https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists/2158532#2158532
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

def ngrams(text, n=2):
    # Creates ngrams of arbitrary size 'n' from a string
    text = text.split()
    ngram_list = (list(zip(*[text[i:] for i in range(n)])))
    ngram_list = [' '.join(tup) for tup in ngram_list]
    return(ngram_list)

def sanatize(text):
    text = text.lower()
    text = text.replace(',', ' ').replace('.', ' ').replace('|', ' ')
    text = text.replace('!', '').replace('?', '')
    text = text.replace('-', ' ').replace('/', ' ')
    text = text.replace('(', '').replace(')', '')
    text = " ".join(text.split()) #Removes whitespace between words
    text = text.strip()
    text = " ".join(text.split())
    return(text)

def extreme_sanatize(text):
    # Removes every non-alphanumeric character and makes lowercase
    text = text.lower()
    text = text.replace(',', ' ').replace('.', ' ') # It is important that these become spaces
    text = text.replace('-', ' ').replace('/', ' ') # to segment the words
    text = ''.join([x for x in text if x.isalnum() or x == ' '])
    text = " ".join(text.split()) #Removes whitespace between words
    return(text)

def get_tuple(term,tup_list):
    # Returns the tuple matching the 1st item
    tup_list = [x for x in tup_list if x[0] == term]
    return(tup_list)
