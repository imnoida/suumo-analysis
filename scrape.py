"""スクレイピングをするモジュール."""
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

site_url = (
    "https://suumo.jp/jj/chintai/ichiran/FR301FC001/"
    "?ar=050&bs=040&ta=23&pc=50&page={}"
)


def request_html(url: str) -> requests.models.Response:
    """指定されたURLのHTMLを取得する.

    :param url: 検索したいURL
    :return: HTML
    """
    return requests.get(url, timeout=10)


def parse_html(url: str) -> BeautifulSoup:
    """指定されたURLのHTMLを解析する.

    :param url: 検索したいURL
    :return: HTML解析用のオブジェクト
    """
    response = request_html(url)
    return BeautifulSoup(response.text, "lxml")


def extract_max_page_number() -> int:
    """最大ページ数を抽出する.

    :return: 最大ページ数
    """
    element = parse_html(site_url.format(1))
    max_page_element = element.select_one("li:nth-child(11) > a")
    max_page = max_page_element.string
    return int(max_page)


def define_url_list(page_number: int, target_url: str) -> list:
    """与えられたページ番号に基づいてURLのリストを生成する.

    :param page_number: ページ数
    :param target_url: 対象のURL
    :return: URLのリスト
    """
    return [target_url.format(page) for page in range(1, page_number + 1)]


def request_multiple_html(page_number: int, target_url: str) -> list:
    """指定されたページ数のURLからHTMLを取得する.

    :param page_number: ページ数
    :param target_url: 対象のURL
    :return: HTMLのリスト
    """
    url_list = define_url_list(page_number, target_url)
    with ThreadPoolExecutor() as executor:
        return list(executor.map(request_html, url_list))


req = request_multiple_html(10, site_url)
