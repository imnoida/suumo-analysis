"""モデルを作成するモジュール."""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

import clean_data
import clean_outlier
from logger import set_logger

if TYPE_CHECKING:
    from logging import Logger

    from pandas import DataFrame


def preprocess_data() -> DataFrame:
    """データの前処理をする.

    :return: 前処理後のDataframe
    """
    cd = clean_data.clean_data().head(50)
    return clean_outlier.clean_outlier(cd)


def encode_categorical_features(
    categorical_features: list,
    cd_cleaned: DataFrame,
) -> tuple:
    """カテゴリカル変数のエンコーディング.

    :param categorical_features: カテゴリカル変数
    :param cd_cleaned: 前処理後のDataframe
    :return: エンコーディングされたカテゴリカル変数
    """
    encoder = OneHotEncoder()
    x_categorical = encoder.fit_transform(cd_cleaned[categorical_features]).toarray()
    return x_categorical, encoder


def made_model(x_train: DataFrame, y_train: DataFrame) -> RandomForestRegressor:
    """モデルの構築.

    :param x_train:
    :param y_train:
    :return:
    """
    rf_model = RandomForestRegressor(random_state=42)
    rf_model.fit(x_train, y_train)
    return rf_model


def evaluate_model_mse(log: Logger, y_pred_rf: DataFrame, y_test: DataFrame) -> None:
    """モデルの評価.

    :param log:
    :param y_pred_rf:
    :param y_test:
    """
    # モデルの評価
    mse_rf = mean_squared_error(y_test, y_pred_rf)
    log.info("ランダムフォレストの平均二乗誤差: %s", mse_rf)


def main() -> None:
    """モデルを作成する."""
    log: Logger = set_logger(module_name=__name__)
    # 説明変数と目的変数の選択
    features = ["築年数", "構造", "階数", "面積", "徒歩"]
    target = "家賃"
    categorical_features = ["地域", "駅", "沿線"]
    cd_cleaned = preprocess_data()
    # 説明変数と目的変数のデータを取得
    x = cd_cleaned[features]
    y = cd_cleaned[target]
    x_categorical, encoder = encode_categorical_features(
        categorical_features,
        cd_cleaned,
    )
    # エンコードされたカテゴリカル変数を結合
    x = np.concatenate((x.to_numpy(), x_categorical), axis=1)
    # 説明変数のリストを更新
    features += encoder.get_feature_names_out(categorical_features).tolist()
    # データの分割
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
    )
    rf_model = made_model(x_train, y_train)
    # テストデータでの予測
    y_pred_rf = rf_model.predict(x_test)
    evaluate_model_mse(log, y_pred_rf, y_test)
    # 実際のデータに予測結果を結合
    cd_cleaned["予測家賃_RF"] = rf_model.predict(x)


main()
