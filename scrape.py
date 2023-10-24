from bs4 import BeautifulSoup
import requests

"""
ar:   area 北海道=10 東北=20 関東=30 甲信越・北陸=40 東海=50 関西=60 四国=70 中国=80 九州・沖縄=90
bs:   マンション新築=10 マンション中古=11 一戸建て新築=20 一戸建て中古 土地=30 賃貸=40
ta:   都道府県ID
pc:   page count
page: page number
"""
target_url = (
    "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=50&bs=40&ta=23&pc=50&page={}"
)


def request_html(url):
    """
    :param url: 検索したいURL
    :return:
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_max_page(url):
    """
    :param url: 検索したいURL
    :return: 最大ページ数
    """
    element = request_html(url)
    max_page_element = element.select_one("li:nth-child(11) > a")
    max_page = max_page_element.string
    return max_page


print(get_max_page(target_url.format(1)))
