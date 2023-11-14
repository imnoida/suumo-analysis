import matplotlib.pyplot as plt
from pandas import DataFrame


def display_plot(cd: DataFrame) -> None:
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
