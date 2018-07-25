# A class to repesent a SNOMED concept

class Concept():

    def __init__(self):
        self.code = None
        self.fsn = None
        self.synonyms = None
        self.parents = None
        self.children = None

    def __repr__(self):
        return(f'{self.fsn} | {self.code}')

    def __str__(self):
        return(f'{self.fsn} | {self.code}')
