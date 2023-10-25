"""スクレイピングをするモジュール."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

import requests
from bs4 import BeautifulSoup, Tag

from logger import set_logger

if TYPE_CHECKING:
    from logging import Logger

site_url: str = (
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
    response: requests.models.Response = request_html(url)
    return BeautifulSoup(response.text, "lxml")


def extract_max_page_number() -> int:
    """最大ページ数を抽出する.

    :return: 最大ページ数
    """
    element: BeautifulSoup = parse_html(site_url.format(1))
    max_page_element: Tag | None = element.select_one("li:nth-child(11) > a")
    msg = "最大ページ数の取得に失敗しました。"
    if max_page_element is None:
        raise ValueError(msg)
    max_page: str | None = max_page_element.string
    if max_page is None:
        raise ValueError(msg)
    return int(max_page)


def generate_url_list(page_number: int, target_url: str) -> list[str]:
    """与えられたページ番号に基づいてURLのリストを生成する.

    :param page_number: ページ数
    :param target_url: 対象のURL
    :return: URLのリスト
    """
    return [target_url.format(page) for page in range(1, page_number + 1)]


def request_multiple_html(
    page_number: int, target_url: str
) -> list[requests.models.Response]:
    """指定されたページ数のURLからHTMLを取得する.

    :param page_number: ページ数
    :param target_url: 対象のURL
    :return: HTMLのリスト
    """
    target_url_list: list[str] = generate_url_list(page_number, target_url)
    with ThreadPoolExecutor() as executor:
        return list[requests.models.Response](
            executor.map(request_html, target_url_list)
        )


req: list[requests.models.Response] = request_multiple_html(10, site_url)
log: Logger = set_logger(module_name="scrape")
log.debug(req)
