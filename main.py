import json
import csv
from bs4 import BeautifulSoup
import requests


class Scraper(requests.Session):
    user_data_template = {
        'url': None,
        'user_handle':None,
        'user_name': None,
        'user_profile_pic_link': None
    }

    def user_metadata_from_post(self, url):
        resp = self.get(url)
        try:
            resp.raise_for_status()
        except requests.HTTPError as err:
            print("{url} ERROR".format(url=err))
            # do we skip or raise?? I think it depends on how the api reacts to the scraping
            js_data = {}
        else:
            js_data = self._extract_js_data_from_resp(resp)
        try:
            owner = js_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']
        except KeyError as err:
            print("Error getting data for url", url)
            print(err)
            print("Mocking the data with `None` values")
            owner = {}

        data = Scraper.user_data_template.copy()
        data['url'] = url
        data['user_handle'] = owner.get('username')
        data['user_name'] = owner.get('full_name')
        data['user_profile_pic_link'] = owner.get('profile_pic_url')

        return data

    @staticmethod
    def _extract_js_data_from_resp(response):
        soup = BeautifulSoup(response.text, 'html5lib')
        raw_js_data = [x
                       for x
                       in soup.find_all('script', type='text/javascript')
                       if x.text.startswith('window._sharedData')][0]

        # turn the tag contents into a json object
        js_data =  json.loads('{{{}}}'.format(raw_js_data.text.split('{', maxsplit=1)[1].rsplit('}', maxsplit=1)[0]))
        return js_data

def main(params):
    pass
