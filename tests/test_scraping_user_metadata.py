import os
import csv
import pytest
import main
from main import Scraper

VALID = {
    "post_url": os.environ['VALID_POST_URL'],
}

INVALID = {
    "post_url": os.environ['INVALID_POST_URL']
}

def test_scraping_valid_post_is_ok():
    scraper = Scraper()
    data = scraper.user_metadata_from_post(VALID['post_url'])
    assert data.keys() == Scraper.user_data_template.keys()
    assert data['user_handle'] not in ('', None)


def test_scraping_invalid_post_returns_empty_data(capsys):
    url = INVALID['post_url']
    scraper = Scraper()
    data = scraper.user_metadata_from_post(url)
    captured = capsys.readouterr()
    assert url + " is private or deleted. Mocking the data with `None` values" in captured.out

    assert data.keys() == Scraper.user_data_template.keys()
    assert data['user_handle'] is None
    assert data['post_link'] == url

def test_scraping_end_to_end_main_function(tmpdir):
    incsv = tmpdir.mkdir('in').mkdir('tables').join(main.FNAME_USER_FROM_POST)
    incsv.write('''post_link,foo
{valid},SOMETHING IGNORED
{invalid},"NOTHINGHERE"'''.format(valid=VALID['post_url'], invalid=INVALID['post_url']))

    tmpdir.mkdir('out').mkdir('tables')

    outpath = main.main(tmpdir.strpath)
    with open(outpath) as outf:
        lines = list(csv.DictReader(outf))

    assert lines[0]['user_handle'] == VALID['post_user_handle']
    assert lines[0]['post_link'] == VALID['post_url']

    assert lines[1]['post_link'] == INVALID['post_url']
    assert lines[1]['user_handle'] == '' # None is translated to empty string

    assert len(lines) == 2
    assert lines[0].keys() == Scraper.user_data_template.keys()
    assert os.path.isfile(str(outpath) + '.manifest')
