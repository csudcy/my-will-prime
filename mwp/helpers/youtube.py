import os

import requests


GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if GOOGLE_API_KEY is None:
    raise Exception('In order to use the Youtube plugin, you must set GOOGLE_API_KEY')


class Youtube(object):

    def find(self, search_query=None, count=10):
        # Query the API
        data = {
            'part': 'snippet',
            'safeSearch': 'moderate',
            'maxResults': count,
            'key': GOOGLE_API_KEY,
            'type': 'video',
        }
        if search_query:
            data['q'] = search_query
        response = requests.get('https://www.googleapis.com/youtube/v3/search', params=data)

        # Return the video URLs
        return [
            'https://www.youtube.com/watch?v={id}'.format(id=item['id']['videoId'])
            for item in response.json()['items']
        ]

if __name__ == '__main__':
    yt = Youtube()
    print yt.find()
    print yt.find()
    print yt.find('how')
    print yt.find('sparta')
