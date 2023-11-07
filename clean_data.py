import re

import pandas as pd
from pandas import DataFrame

df: DataFrame = pd.read_csv("data/scrape.csv")


def extract_number(value: str) -> float:
    n = re.findall(r"[\d.]+", value)
    if len(n) == 0:
        return 0
    return float(n[0])


df["家賃"] = df["家賃"].apply(extract_number)
df["管理費"] = df["管理費"].apply(extract_number)
df["管理費"] /= 10000
df["敷金"] = df["敷金"].apply(extract_number)
df["礼金"] = df["礼金"].apply(extract_number)
df["面積"] = df["面積"].apply(extract_number)
df["築年数"] = df["築年数"].apply(extract_number)
df = df.dropna(subset=["アクセス"])
df["沿線"] = df["アクセス"].apply(lambda x: x.split("/")[0])
df = df.query("沿線.str.contains('線') & ~沿線.str.contains('バス')")

df.plot()
