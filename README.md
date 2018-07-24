SNOMEDCT_mapper
==========

Python tool to map free text to SNOMED CT terms using fuzzy string matching

Requirements
============
-  Python 3
-  `fuzzywuzzy <https://github.com/seatgeek/fuzzywuzzy/>`_ ``pip install fuzzywuzzy[speedup]``
-  pandas

Usage
=====
.. code:: python

    >>> from mapper import Mapper
    >>> m = Mapper('indicated for treatment of heart attack and hypertension')
    >>> m.standard_search()  # Returns a pandas DataFrame with the matched terms

       Term              ID
    0  htn hypertension  38341003
    1      heart attack  22298006
