""" Advent of Code 2017, Day 4 tests """
from passphrases import has_no_duplicates, has_no_anagrams


def test_has_no_duplicates():
    assert has_no_duplicates('aa bb cc dd ee')
    assert not has_no_duplicates('aa bb cc dd aa')
    assert has_no_duplicates('aa bb cc dd aaa')


def test_has_no_anagrams():
    assert has_no_anagrams('abcde fghij')
    assert not has_no_anagrams('abcde xyz ecdab')
    assert has_no_anagrams('a ab abc abd abf abj')
    assert has_no_anagrams('iiii oiii ooii oooi oooo')
    assert not has_no_anagrams('oiii ioii iioi iiio')
