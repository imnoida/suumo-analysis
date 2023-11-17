import re

import pandas as pd
from pandas import DataFrame


def extract_number(value: str) -> float:
    n = re.findall(r"[\d.]+", value)
    return float(n[0]) if n else 0


def extract_location(value: str) -> str:
    n = re.search(r"愛知県(.*?郡|名古屋市.*?区|.*?市)", value)
    return n.group(1) if n else "NaN"


def extract_station(line: str) -> str:
    return line.split(" ")[0].split("/")[1]


def extract_walk_distance(line: str) -> int:
    return int(re.findall(r"\d+", line.split(" ")[1])[0])


def clean_data() -> DataFrame:
    df: DataFrame = pd.read_csv("data/scrape.csv")
    df["構造"] = df["構造"].apply(extract_number)
    df["階数"] = df["階数"].apply(extract_number)
    df["家賃"] = df["家賃"].apply(extract_number)
    df["管理費"] = df["管理費"].apply(extract_number) / 10000
    df["敷金"] = df["敷金"].apply(extract_number)
    df["礼金"] = df["礼金"].apply(extract_number)
    df["面積"] = df["面積"].apply(extract_number)
    df["築年数"] = df["築年数"].apply(extract_number)
    df = df.dropna(subset=["アクセス"])
    df["沿線"] = df["アクセス"].apply(lambda x: x.split("/")[0])
    df = df[df["沿線"].str.contains("線") & ~df["沿線"].str.contains("バス")]
    df["駅"] = df["アクセス"].apply(extract_station)
    df = df[df["アクセス"].str.contains("歩") & ~df["アクセス"].str.contains("バス")]
    df["徒歩"] = df["アクセス"].apply(extract_walk_distance)
    df["地域"] = df["アドレス"].apply(extract_location)
    return df
