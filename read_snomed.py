import pandas as pd
from pathlib import Path

data_folder = Path("snomed_data")

def csv_to_tup_list(filename):
    # Read in the SNOMED CSV files as named tuples
    # Each is labeled as a "Synonym" and have the form ("term", "code")
    df = pd.read_csv(filename, sep=',', header=None)
    df.columns = ["term", "code"] #Rename columns
    df['term'].apply(lambda x: str(x))
    df['code'].apply(lambda x: int(x))
    tup_list = []
    for row in df.itertuples(index=False, name="Synonym"):
         tup_list.append(row)
    tup_list = [x for x in tup_list if type(x.term) == str]
    return (tup_list)

def load_lexicon(lexicon_name):
    # Loads a SNOMED lexicon and returns the data as a list of tuples
    extra_terms = csv_to_tup_list(data_folder / 'extra_terms.csv')

    names = ['full', 'my_acronyms', 'findings', 'disorders', 'recommended']
    if lexicon_name not in names:
        raise ValueError('Invalid lexicon name provided!')
    filename = lexicon_name + '.csv'
    lexicon = csv_to_tup_list(data_folder / filename) + extra_terms
    return(lexicon)
