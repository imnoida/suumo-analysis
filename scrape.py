"""スクレイピングをするモジュール."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag
from tenacity import retry, wait_exponential
from tqdm import tqdm

from logger import set_logger

if TYPE_CHECKING:
    from logging import Logger

log: Logger = set_logger(module_name=__name__)
site_url: str = (
    "https://suumo.jp/jj/chintai/ichiran/FR301FC001/"
    "?ar=050&bs=040&ta=23&pc=50&page={}"
)


@retry(wait=wait_exponential(multiplier=1, min=1, max=60))
def request_html(url: str) -> requests.models.Response:
    """指定されたURLのHTMLを取得する.

    :param url: 検索したいURL
    :return: HTML
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response


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


def generate_url_list(page_number: int) -> list[str]:
    """与えられたページ番号に基づいてURLのリストを生成する.

    :param page_number: ページ数
    :return: URLのリスト
    """
    return [site_url.format(page) for page in range(1, page_number + 1)]


def parse_multiple_html(page_number: int) -> list[BeautifulSoup]:
    """指定されたページ数のURLからHTMLを取得する.

    :param page_number: ページ数
    :return: HTMLのリスト
    """
    target_url_list: list[str] = generate_url_list(page_number)
    with ThreadPoolExecutor() as executor:
        progress: tqdm[BeautifulSoup] = tqdm(
            executor.map(parse_html, target_url_list),
            total=len(target_url_list),
        )
        progress.set_description("parse_multiple_html")
        result: list[BeautifulSoup] = list(progress)
        return result


def extract_additional_data(
    item: BeautifulSoup,
    base_data: dict[str, str],
) -> list[dict[str, str]]:
    """追加のデータを抽出する.

    :param item: HTML
    :param base_data: 基本のデータ
    :return:
    """
    tbodys: list[BeautifulSoup] = item.find(
        "table",
        {"class": "cassetteitem_other"},
    ).findAll("tbody")
    additional_data: list[dict[str, str]] = []
    for tbody in tbodys:
        data = base_data.copy()
        columns = tbody.findAll("td")
        data["階数"] = columns[2].getText().strip()
        rent_info = columns[3].findAll("li")
        data["家賃"] = rent_info[0].getText().strip()
        data["管理費"] = rent_info[1].getText().strip()
        deposit_info = columns[4].findAll("li")
        data["敷金"] = deposit_info[0].getText().strip()
        data["礼金"] = deposit_info[1].getText().strip()
        layout_info = columns[5].findAll("li")
        data["間取り"] = layout_info[0].getText().strip()
        data["面積"] = layout_info[1].getText().strip()
        data["URL"] = f"https://suumo.jp{columns[8].find('a').get('href')}"

        additional_data.append(data)
    return additional_data


def extract_base_data(item: BeautifulSoup, stations: list[Tag]) -> list[dict[str, str]]:
    """基本のデータを抽出する.

    :param item: HTML
    :param stations: 駅リスト
    :return:
    """
    base_data: dict[str, str] = {
        "名称": item.find("div", {"class": "cassetteitem_content-title"})
        .getText()
        .strip(),
        "カテゴリー": item.find("div", {"class": "cassetteitem_content-label"})
        .getText()
        .strip(),
        "アドレス": item.find("li", {"class": "cassetteitem_detail-col1"})
        .getText()
        .strip(),
        "アクセス": stations[0].getText().strip(),
        "築年数": item.find("li", {"class": "cassetteitem_detail-col3"})
        .findAll("div")[0]
        .getText()
        .strip(),
        "構造": item.find("li", {"class": "cassetteitem_detail-col3"})
        .findAll("div")[1]
        .getText()
        .strip(),
    }
    return extract_additional_data(item, base_data)


def extract_elements() -> list[dict[str, str]]:
    """要素を抽出する.

    :return: 要素
    """
    all_data: list[dict[str, str]] = []
    page_number: int = extract_max_page_number()
    list_html: list[BeautifulSoup] = parse_multiple_html(page_number)
    for html in list_html:
        items: list[BeautifulSoup] = html.findAll("div", {"class": "cassetteitem"})
        for item in items:
            stations: list[Tag] = item.findAll(
                "div",
                {"class": "cassetteitem_detail-text"},
            )
            additional_data: list[dict[str, str]] = extract_base_data(item, stations)
            all_data.extend(additional_data)
    log.debug("完了")
    return all_data


def save_to_csv() -> None:
    """csvにデータを保存する."""
    dataframe: pd.DataFrame = pd.DataFrame(extract_elements())
    Path("data").mkdir(parents=True, exist_ok=True)
    dataframe.to_csv("data/scrape.csv")
    log.debug("スクレイピング完了")
