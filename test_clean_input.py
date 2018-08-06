from clean_input import clean_input

def test_clean_input():

    # Test some cleaning examples
    test_text = 'indicated for heart attack and cancer in pediatric patients'
    assert(clean_input(test_text) == 'heart attack cancer')

    test_text = 'Schizophrenia and lung CanCeR treatment'
    assert(clean_input(test_text) == 'schizophrenia lung cancer')
