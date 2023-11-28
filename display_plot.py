import matplotlib.pyplot as plt
from pandas import DataFrame
import numpy as np

def average_rent_graph(cd: DataFrame) -> None:
    average_rent_per_city = cd.groupby("地域")["家賃"].mean()
    x = average_rent_per_city.index
    y = average_rent_per_city.to_numpy()
    plt.rcParams["font.family"] = "MS Gothic"
    plt.figure(figsize=(12, 16))
    plt.title("地域ごとの平均家賃")
    plt.xticks()
    plt.yticks()
    plt.xlabel("平均家賃")
    plt.ylabel("地域")
    plt.grid()
    plt.barh(x, y)
    plt.show()


def rent_hist(cd: DataFrame) -> None:
    base_bins = round(cd["家賃"].max() - cd["家賃"].min())
    bins = base_bins * 5
    ranges = (round(cd["家賃"].min()), round(cd["家賃"].max()))
    plt.rcParams["font.family"] = "MS Gothic"
    plt.figure(figsize=(16, 9))
    plt.title("家賃の分布")
    plt.xticks(np.arange(0, 11, 1))
    plt.yticks()
    plt.xlabel("家賃")
    plt.ylabel("件数")
    plt.grid()
    plt.hist(cd["家賃"], bins=bins, range=ranges)
    plt.show()
