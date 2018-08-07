from helper_tools import sanatize, remove_words, get_words_from_csv
import spacy
nlp = spacy.load('en_core_web_lg')

def clean_input(string):
    '''
    Reduces the input string to the essential words needed for SNOMED CT matching
    Returns `str`
    '''

    # Sanatize the string
    string = sanatize(string)

    doc = nlp(string)
    string = ' '.join([np.text for np in doc.noun_chunks])

    # Remove dictionary words not in SNOMED CT
    doc = nlp(string)
    dict_remove_strings = set(get_words_from_csv('dict_remove_strings_recommended.csv'))
    string = ' '.join([x.text for x in doc if x.lemma_ not in dict_remove_strings])

    # Remove curated words
    curated_remove_strings = set(get_words_from_csv('curated_remove_strings.csv'))
    string = remove_words(string, curated_remove_strings)

    # Remove stopwords
    stopwords = set(get_words_from_csv('stopwords.csv'))
    string = remove_words(string, stopwords)

    # Sanatize
    string = sanatize(string)

    return string
