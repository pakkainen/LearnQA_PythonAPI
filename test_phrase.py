import pytest

phrase = input("Please, set a phrase shorter than 15 characters: ")
assert len(phrase) < 15, "Your phrase is not shorter than 15 characters"