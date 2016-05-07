import json
import os
import requests
import random

# Number of deals to get in order to choose a maximum (30 is max supported by API without pagination)
RANDOM_RANGE = 30
HUKD_API_KEY = os.environ.get('HUKD_API_KEY')
if HUKD_API_KEY is None:
    raise Exception('In order to use hot deals, you must set HUKD_API_KEY')

class Dealer(object):
    def make_request(self, type, results):
        payload = {
            'key': HUKD_API_KEY,
            'output': 'json',
            'forum': 'deals',
            'results_per_page': results,
            'order': type,
        }
        return requests.get('http://api.hotukdeals.com/rest_api/v2/', params=payload).json()

    def get_deal(self, type='hot'):
        if type not in ('new', 'hot', 'random'):
            return "Sorry, I only support new, hot or random deals!"

        if type == 'random':
            deal = self.make_request('hot', RANDOM_RANGE)['deals']['items'][random.randint(0,RANDOM_RANGE-1)]
        else:
            deal = self.make_request(type, 1)['deals']['items'][0]

        return "[%s by %s] %s: %s" % (deal['submit_time'], deal['poster_name'], deal['title'], deal['deal_link'])

if __name__ == '__main__':
    d = Dealer()
    print d.get_deal()
    print d.get_deal(type='new')
    print d.get_deal(type='random')
