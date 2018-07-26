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

def remove_words(string, remove_string_or_list):
    """
    Removes the strings in remove_string_or_list from string
    Input: (string, string or list of strings)
    Output: string
    """
    str_list = string.split(' ')
    if isinstance(remove_string_or_list, str):
        str_list = [word for word in str_list if word != remove_string_or_list]
    elif remove_string_or_list and all(isinstance(s, str) for s in remove_string_or_list):
        str_list = [word for word in str_list if word not in remove_string_or_list]
    else:
        raise ValueError('Input was not a string or a list of strings')

    cleaned_str = ' '.join(str_list)
    assert(isinstance(cleaned_str, str))
    return(' '.join(str_list))

