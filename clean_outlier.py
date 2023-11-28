from pandas import DataFrame


def clean_outlier(df: DataFrame) -> DataFrame:
    mu = df["家賃"].mean()
    sigma = df["家賃"].std()
    df = df[(mu - 3 * sigma < df["家賃"]) & (df["家賃"] < mu + 3 * sigma)]
    return df
