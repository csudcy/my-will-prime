# https://en.wikipedia.org/w/api.php?

import requests


class Wikipedia(object):

    def find(self, search_query):
        # Query the API
        data = {
            'action': 'opensearch',
            'limit': 1,
            'namespace': 0,
            'format': 'json',
            'search': search_query,
        }
        response = requests.get('https://en.wikipedia.org/w/api.php', params=data)

        # Return the page URLs
        result_urls = response.json()[3]
        if result_urls:
            return result_urls[0]
        return None

if __name__ == '__main__':
    wp = Wikipedia()
    print wp.find('age')
    print wp.find('football')
    print wp.find('how')
    print wp.find('sparta')
