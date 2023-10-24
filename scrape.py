from bs4 import BeautifulSoup
import requests


target_url = (
    "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=50&bs=40&ta=23&pc=50&page={}"
)


def request_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_max_page(url):
    element = request_html(url)
    max_page_element = element.select_one("li:nth-child(11) > a")
    max_page = max_page_element.string
    return max_page


print(get_max_page(target_url.format(1)))
