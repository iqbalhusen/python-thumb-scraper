from lxml import html
import requests
import json
from requests.auth import HTTPBasicAuth

ENTRY_PAGE_URL = 'https://yolaw-tokeep-hiring-env.herokuapp.com/'
BASIC_AUTH_USERNAME = 'Thumb'
BASIC_AUTH_PASSWORD = 'Scraper'

with open('input_tampered.json') as f:
    input_data = json.load(f)


def main():
    next_url = ENTRY_PAGE_URL
    for index, key in enumerate(input_data):
        page = requests.get(next_url, auth=HTTPBasicAuth(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD))
        tree = html.fromstring(page.content)

        xpath_test_result = tree.xpath(input_data[key]['xpath_test_query'])
        if xpath_test_result == input_data[key]['xpath_test_result']:
            print('Move to page %d' % (index + 1))
        else:
            print('ALERT - Can’t move to page %d: page %d link has been malevolently tampered with!!' % (
                index + 1,
                index
            ))

        xpath_button_to_click = tree.xpath(input_data[key]['xpath_button_to_click'] + '/@href')
        next_url = ENTRY_PAGE_URL + xpath_button_to_click[0]


if __name__ == '__main__':
    main()
