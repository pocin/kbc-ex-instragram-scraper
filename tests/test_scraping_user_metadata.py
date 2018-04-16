import os
from main import Scraper

VALID = {
    "post_url": os.environ['VALID_POST_URL'],
    "post_user_handle": os.environ['VALID_USER_HANDLE']
}

# INVALID = {
#     "post_url": 'https://www.instagram.com/p/BhlUmAjnzSS/#1337_1757901802426021010_1967348397'
# }

def test_scraping_valid_post_is_ok():
    scraper = Scraper()
    data = scraper.user_metadata_from_post(VALID['post_url'])
    assert data.keys() == Scraper.user_data_template.keys()
    assert data['user_handle'] == VALID['post_user_handle']
