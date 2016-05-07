import json
import os
import random

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_PATH = os.path.split(CURRENT_PATH)[0]
DATA_FILE = os.path.join(PARENT_PATH, 'data', 'buzzwords.json')


class Business(object):
    def __init__(self, *args, **kwargs):
        # Load the buzzwords
        with open(DATA_FILE) as f:
            self.buzzwords = json.load(f)

    def acquire_business(self):
        business = '{before1} {before2} {noun} {after} '.format(
            before1=random.choice(self.buzzwords['before']),
            before2=random.choice(self.buzzwords['before']),
            noun=random.choice(self.buzzwords['nouns']),
            after=random.choice(self.buzzwords['after']),
        ).title()
        return business

if __name__ == '__main__':
    b = Business()
    print b.acquire_business()
    print b.acquire_business()
    print b.acquire_business()
