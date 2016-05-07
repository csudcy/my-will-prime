import json
import os
import random

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_PATH = os.path.split(CURRENT_PATH)[0]
DATA_FILE = os.path.join(PARENT_PATH, 'data', 'dictionary.json')


class Dictionary(object):
    def __init__(self):
        # Load the dictionary
        with open(os.path.abspath(DATA_FILE), 'r') as f:
            self._dict = json.load(f)

    def get_dict(self):
        return self._dict

    def get_random_definition(self):
        word = random.choice(self._dict.keys())
        return self.get_definition(word)

    def get_definition(self, word):
        if word.upper() in self._dict:
            return '{0}: {1}'.format(word.title(), self._dict[word.upper()])
        else:
            return '{0} isn\'t a word you numpty'.format(word.title())

if __name__ == '__main__':
    dm = Dictionary()
    print dm.get_definition('diploblastic')
    print dm.get_definition('asdfasdf')
    print dm.get_random_definition()
