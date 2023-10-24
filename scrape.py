"""
スクレイピングをするモジュール
"""
from bs4 import BeautifulSoup
import requests

"""
ar:   area 北海道=010 東北=020 関東=030 甲信越・北陸=040 東海=050 関西=060 四国=070 中国=080 九州・沖縄=090
bs:   マンション新築=010 マンション中古=011 一戸建て新築=020 一戸建て中古 土地=030 賃貸=040
ta:   都道府県ID
pc:   page count
page: page number
"""
target_url = (
    "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=050&bs=040&ta=23&pc=50&page={}"
)

url_list = []


def request_html(url):
    return requests.get(url)


def parse_html(url):
    """
    :param url: 検索したいURL
    :return: HTML解析用のオブジェクト
    """
    response = request_html(url)
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def extract_max_page_number():
    """
    :return: 最大ページ数
    """
    element = parse_html(target_url.format(1))
    max_page_element = element.select_one("li:nth-child(11) > a")
    max_page = max_page_element.string
    return int(max_page)


def define_url_list(page_number):
    for page in range(1, page_number + 1):
        url_list.append(target_url.format(page))



print(extract_max_page_number(target_url.format(1)))
