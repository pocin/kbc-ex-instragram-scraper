import json
import os
import sys
import traceback
import csv
from bs4 import BeautifulSoup
from pathlib import Path
import requests

FNAME_USER_FROM_POST = 'user_metadata_from_posts.csv'

class Scraper(requests.Session):
    user_data_template = {
        'post_link': None,
        'user_handle':None,
        'user_name': None,
        'user_profile_pic_link': None
    }

    def user_metadata_from_post(self, url):
        resp = self.get(url)
        try:
            resp.raise_for_status()
        except requests.HTTPError as err:
            # do we skip or raise?? I think it depends on how the api reacts to the scraping
            if resp.status_code == 404:
                print(url, "is private or deleted. Mocking the data with `None` values")
                owner = {}
            else:
                # blacklist/whatever error? TODO: need to figure this out
                raise
        else:
            try:
                js_data = self._extract_js_data_from_resp(resp)
            except IndexError:
                print("Error getting data from js variable for post", url)
                owner = {}
            else:
                try:
                    owner = js_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']
                except KeyError as err:
                    raise ValueError("Error getting data for ",
                                     url,
                                     "despite it should be ok. CHECK THIS POST MANUALLY")

        data = Scraper.user_data_template.copy()
        data['post_link'] = url
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

def main(datadir='/data'):
    scraper = Scraper()
    inpath = Path(datadir) / 'in/tables/' / FNAME_USER_FROM_POST
    outpath = Path(datadir) / 'out/tables' / FNAME_USER_FROM_POST
    # we use scraper as context manager to reuse underlying tcp connection
    with open(inpath, 'r') as inf,  open(outpath, 'w') as outf,  scraper:
        reader = csv.DictReader(inf)
        writer = csv.DictWriter(outf, fieldnames=scraper.user_data_template.keys())
        writer.writeheader()
        for post in reader:
            data = scraper.user_metadata_from_post(post['post_link'])
            writer.writerow(data)

    with open(str(outpath) + '.manifest', 'w') as manif:
        json.dump({"incremental": True, "primary_key": ["post_link"]}, manif)

    return outpath


if __name__ == "__main__":
    try:
        main(os.environ['KBC_DATADIR'])
    except (KeyError, ValueError, requests.ConnectionError, requests.HTTPError) as err:
        print(err)
        sys.exit(1)
    except:
        traceback.print_exc()
        sys.exit(2)


