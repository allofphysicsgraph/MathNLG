from unittest import TestCase, skip
from paramunittest import parametrized

from nlg.tools import load, parse, diffFormat, skipTest, assertEqual

first_occurence_data = load('tests/data/first_occurence_data.json')
first_occurence_meta = load('tests/data/first_occurence_meta.json')
first_occurence_tests = load('tests/data/first_occurence_tests.json')

print first_occurence_data
print first_occurence_meta
print first_occurence_tests
