from mapper import Mapper

def test_standard_search():

    # Assert that heart attack (22298006) and cancer (363346000) are matched
    test_text = 'heart attack and cancer'
    m = Mapper(test_text)
    df = m.standard_search()
    assert(22298006 in m.codes)
    assert(363346000 in m.codes)

    # Test extra_terms with diabetes (73211009)
    test_text = 'diabetes'
    m = Mapper(test_text)
    df = m.standard_search()
    assert(73211009 in m.codes)

    test_text = 'diabetez'
    m = Mapper(test_text)
    df = m.standard_search()
    assert(73211009 in m.codes)

    # Test acronym matcher
    test_text = 't2dm'
    m = Mapper(test_text)
    df = m.standard_search()
    assert(44054006 in m.codes)

    test_text = 'nash'
    m = Mapper(test_text)
    df = m.standard_search()
    assert(442685003 in m.codes)

    # Test user defined terms
    test_text = 'antidepressant'
    m = Mapper(test_text)
    df = m.standard_search()
    assert(35489007 in m.codes)
