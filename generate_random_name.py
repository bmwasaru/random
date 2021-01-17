"""
Generate a random user name using the string python library, use range to determine desired length of name.
Use case could be need to generate a user name when doing tests
"""
import string
import random


def random_name():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
