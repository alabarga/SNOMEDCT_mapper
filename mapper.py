import pandas as pd
from fuzzywuzzy import process, fuzz
from read_snomed import load_lexicon
from helper_tools import ngrams, sanatize, get_tuple, flatten, group, remove_words
from collections import namedtuple

#---------------------------------------------------------------------------------------------
# GLOBAL PARAMETERS
SCORER_LIMIT = 87 # Sets the sensitivity of the FuzzyWuzzy matcher (Lower = more false positives)
MAX_NGRAM_SIZE = 6 # Sets the maximum ngram size tested (Higher = slower)
MAX_DISTANCE = 8 # Sets the maximum length difference possible for a match (Higher = slower)
USE_REMOVE = True # Sets if the fuzzy search removes terms as it finds them
STANDARD_LEXICON = "disorders" # Sets the standard subset of the SNOMED database to use
#---------------------------------------------------------------------------------------------

class Mapper:
    def __init__(self, text, lexicon = STANDARD_LEXICON):
        self.text = sanatize(text)
        self.original_text = text # We leave this unmodified by other functions
        self.lexicon = load_lexicon(lexicon)
        self.matches = set() # Matched ID's are added here
        self.matches_w_score = set() # For debugging and sorting

    @property
    def codes(self):
        return(x.code for x in self.matches)

    def __str__(self):
        return(f"Original text is: {self.original_text}\nCurrent text is: {self.text}")

    def __repr__(self):
        return(f"Original text is: {self.original_text}\nCurrent text is: {self.text}")

    def remove(self,string):
        # Removes the string from self.text
        self.text = self.text.replace(string,' ')

    def get_num_words(self):
        # Gets the current number of words in the text
        text_list = self.text.split(' ')
        length = len(text_list)
        return(length)

    def get_max_ngram(self):
        # get the maximum ngram size needed
        length = self.get_num_words()
        if length < MAX_NGRAM_SIZE:
            return(length)
        else:
            return(MAX_NGRAM_SIZE)

    def cut_lexicon(self, query):
        # Returns a lexicon that is cut down to words within max_distance of the query
        length  = len(query)
        upper = length + MAX_DISTANCE
        lower = length - MAX_DISTANCE
        reduced_lexicon = [syn for syn in self.lexicon if lower <= len(syn.term) <= upper]
        return(reduced_lexicon)

    def exact_search(self):
        # Matches only on exact strings
        length = self.get_num_words()
        for i in range(MAX_NGRAM_SIZE,0,-1): # Iterates through all ngram lengths up to the MAX_NGRAM_SIZE
            ngram_list = ngrams(self.text,i)
            for ngram in ngram_list:
                new_lexicon = [x for x in self.lexicon if x.term == ngram]
                for syn in new_lexicon:
                    self.matches.add(syn)
                    self.matches_w_score.add((syn, 'NA', "exact"))

    def acronym_search(self):
        # Matches against the acronym list
        acronyms = load_lexicon("my_acronyms")
        length = self.get_num_words()

        for i in range(length,0,-1):
            ngram_list = ngrams(self.text,i)
            for ngram in ngram_list:
                new_lexicon = [x for x in acronyms if x.term == ngram]
                for syn in new_lexicon:
                    self.matches.add(syn)
                    tup_w_score = namedtuple('matches_w_score', ['ngram','tup', 'score','scorer_name'])
                    self.matches_w_score.add(tup_w_score(syn[0], syn, 'NA', 'acronym'))

    def fuzzy_match(self, query, reduced_lexicon, limit=SCORER_LIMIT):
        # Matches against the SNOMED lexicon using fuzzy string matching

        terms = [x.term for x in reduced_lexicon]

        result_sort = process.extractOne(query, terms, scorer=fuzz.token_sort_ratio)
        result_sort = (result_sort[0], result_sort[1] - 10) #Rank result sort a bit lower than ratio

        result_ratio = process.extractOne(query, terms, scorer=fuzz.ratio)

        if result_sort[1] >= result_ratio[1]:
            result = result_sort
            scorer_name = "sort"
        else:
            result = result_ratio
            scorer_name = "ratio"

        if result[1] >= limit: #if the returned score is greater or equal to than the cutoff value
            return((get_tuple(result[0], reduced_lexicon), result[1], scorer_name)) # Returns a list of matched synonyms
        else:
            return(False)

    def fuzzy_search(self):
        max_ngram = self.get_max_ngram()
        for i in range(max_ngram,0,-1):
            ngram_list = ngrams(self.text,i)
            for ngram in ngram_list:
                reduced_lexicon = self.cut_lexicon(ngram)
                result = self.fuzzy_match(ngram,reduced_lexicon)

                if result:
                    tups = self.fuzzy_match(ngram,reduced_lexicon)[0]
                    score = self.fuzzy_match(ngram,reduced_lexicon)[1]
                    scorer_name = self.fuzzy_match(ngram,reduced_lexicon)[2]

                    for tup in tups:
                        self.matches.add(tup)
                        tup_w_score = namedtuple('matches_w_score', ['ngram','tup', 'score','scorer_name'])
                        self.matches_w_score.add(tup_w_score(ngram, tup, score, scorer_name))

                    if USE_REMOVE == True:
                        self.remove(ngram)
                        self.text = sanatize(self.text)

    def to_df(self, show_scores = False):
        # Returns self.matches as a Pandas DataFrame

        if show_scores == True:
            matches = list(group(list(flatten(list(self.matches_w_score))),5))
            df = pd.DataFrame(matches)

            if df.empty != True:
                df.columns = ['ngram', 'Term', 'ID', 'Score', 'Name']
                s = df.Term.str.len().sort_values(ascending=False).index
                df = df.reindex(s)
                df.reset_index(inplace=True, drop=True)
                return(df)
            else:
                return(pd.DataFrame([])) # Return an empty DataFrame

        else:
            matches = list(self.matches)
            df = pd.DataFrame(matches)

            if df.empty != True:
                df.columns = ['Term', 'ID']
                s = df.Term.str.len().sort_values(ascending=False).index
                df = df.reindex(s)
                df.reset_index(inplace=True, drop=True)
                return(df)
            else:
                return(pd.DataFrame([])) # Return an empty DataFrame

    def standard_search(self, show_scores = False):
        # Convenience function - the standard sequence of search functions
        # Returns matches as a Pandas DataFrame
        self.acronym_search()
        self.fuzzy_search()
        return(self.to_df(show_scores))

    def rapid_search(self):
        # Acronym search + exact search
        self.acronym_search()
        self.exact_search()
        return(self.to_df())
