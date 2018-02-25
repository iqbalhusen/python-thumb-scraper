from lxml import html
import requests
import json
from requests.auth import HTTPBasicAuth

ENTRY_PAGE_URL = 'https://yolaw-tokeep-hiring-env.herokuapp.com'
BASIC_AUTH_USERNAME = 'Thumb'
BASIC_AUTH_PASSWORD = 'Scraper'

with open('data/input_tampered.json') as f:
    input_data = json.load(f)


def main():
    url = ENTRY_PAGE_URL
    key = next(iter(input_data))
    index = 0

    while index < len(input_data):
        page = requests.get(url, auth=HTTPBasicAuth(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD))
        tree = html.fromstring(page.content)

        xpath_test_result = tree.xpath(input_data[key]['xpath_test_query'])
        next_page_url_paths = tree.xpath(input_data[key]['xpath_button_to_click'] + '/@href')

        if xpath_test_result == input_data[key]['xpath_test_result'] and next_page_url_paths:
            print('Move to page %d' % (index + 1))
        else:
            print('ALERT - Can’t move to page %d: page %d link has been malevolently tampered with!!' % (
                index + 1,
                index
            ))
            break

        url = ENTRY_PAGE_URL + next_page_url_paths[0]
        key = input_data[key]['next_page_expected']
        index += 1


if __name__ == '__main__':
    main()
