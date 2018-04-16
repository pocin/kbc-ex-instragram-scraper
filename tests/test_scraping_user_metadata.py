import os
import pytest
from main import Scraper

VALID = {
    "post_url": os.environ['VALID_POST_URL'],
    "post_user_handle": os.environ['VALID_USER_HANDLE']
}

INVALID = {
    "post_url": os.environ['INVALID_POST_URL']
}

def test_scraping_valid_post_is_ok():
    scraper = Scraper()
    data = scraper.user_metadata_from_post(VALID['post_url'])
    assert data.keys() == Scraper.user_data_template.keys()
    assert data['user_handle'] == VALID['post_user_handle']


def test_scraping_invalid_post_returns_empty_data(capsys):
    url = INVALID['post_url']
    scraper = Scraper()
    data = scraper.user_metadata_from_post(url)
    captured = capsys.readouterr()
    assert "Mocking the data with `None` values" in captured.out
    assert "Error getting data for url " + url in captured.out

    assert data.keys() == Scraper.user_data_template.keys()
    assert data['user_handle'] is None
    assert data['url'] == url
