"""モデルを作成するモジュール."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import joblib
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

    from pandas import DataFrame, Series

log: Logger = set_logger(module_name=__name__)


def preprocess_data() -> DataFrame:
    """データの前処理をする.

    :return: 前処理後のDataframe
    """
    cd = clean_data.clean_data().head(50)
    return clean_outlier.clean_outlier(cd)


def encode_categorical_features(
    categorical_features: list[str],
    cd_cleaned: DataFrame,
) -> np.ndarray:
    """カテゴリカル変数のエンコーディング.

    :param categorical_features: カテゴリカル変数
    :param cd_cleaned: 前処理後のDataframe
    :return: エンコーディングされたカテゴリカル変数
    """
    encoder = OneHotEncoder()
    return encoder.fit_transform(cd_cleaned[categorical_features]).toarray()


def save_model(rf_model: RandomForestRegressor, path: Path) -> None:
    """モデルを保存する.

    :param rf_model: モデル
    :param path: 保存先
    """
    Path("model").mkdir(parents=True, exist_ok=True)
    joblib.dump(rf_model, path)


def load_model(x_train: DataFrame, y_train: DataFrame) -> RandomForestRegressor:
    """モデルの読み込み.

    :param x_train: 訓練データ
    :param y_train: 訓練データ
    :return: モデル
    """
    model_path = Path("model")
    model_path.mkdir(parents=True, exist_ok=True)
    rf_model_path = model_path / "rf_model.joblib"
    if rf_model_path.exists():
        rf_model = joblib.load(rf_model_path)
    else:
        rf_model = made_model(x_train, y_train)
        save_model(rf_model, rf_model_path)
    return rf_model


def made_model(x_train: DataFrame, y_train: DataFrame) -> RandomForestRegressor:
    """モデルの構築.

    :param x_train: 訓練用説明データ
    :param y_train: 訓練用目的データ
    :return: モデル
    """
    rf_model = RandomForestRegressor(random_state=42)
    rf_model.fit(x_train, y_train)
    return rf_model


def evaluate_model_mse(y_pred_rf: DataFrame, y_test: DataFrame) -> None:
    """モデルの評価.

    :param y_pred_rf: モデルの予測値
    :param y_test: 訓練用目的データ
    """
    mse_rf = mean_squared_error(y_test, y_pred_rf)
    log.info("ランダムフォレストの平均二乗誤差: %s", mse_rf)


def save_to_csv(cd_cleaned: DataFrame) -> None:
    """データをcsvに保存.

    :param cd_cleaned: 前処理後のDataframe
    """
    data_path = Path("data")
    data_path.mkdir(parents=True, exist_ok=True)
    cd_cleaned.to_csv(data_path / "rf_predict.csv")


def select_features_and_target(
    data: DataFrame,
    features: list[str],
    target: str,
) -> tuple[DataFrame | Series, Series]:
    """説明変数と目的変数のデータを取得.

    :param data: 前処理後のDataframe
    :param features: 取得する説明変数のリスト
    :param target: 取得する目的変数
    :return: 説明変数と目的変数
    """
    return data[features], data[target]


def combine_features_with_encoded_categorical(
    x: DataFrame,
    x_categorical: np.ndarray,
) -> np.ndarray:
    """エンコードされた説明変数を結合.

    :param x: 説明変数
    :param x_categorical: エンコードされた説明変数
    :return: 結合した説明変数
    """
    return np.concatenate((x.to_numpy(), x_categorical), axis=1)


def update_feature_list(
    features: list[str],
    encoder: OneHotEncoder,
    categorical_features: list[str],
) -> list[str]:
    """説明変数のリストを更新.

    :param features: 更新前の説明変数のリスト
    :param encoder: エンコーダー
    :param categorical_features: エンコードされた説明変数のリスト
    :return: 更新後の説明変数のリスト
    """
    return features + encoder.get_feature_names_out(categorical_features).tolist()


def split_data(x: np.ndarray, y: Series) -> tuple:
    """データの分割.

    :param x: 説明変数
    :param y: 目的変数
    :return: 訓練データと検証データ
    """
    return train_test_split(x, y, test_size=0.2, random_state=42)


def main() -> None:
    """モデルを作成する."""
    features = ["築年数", "構造", "階数", "面積", "徒歩"]
    target = "家賃"
    categorical_features = ["地域", "駅", "沿線"]
    cd_cleaned = preprocess_data()
    x, y = select_features_and_target(cd_cleaned, features, target)
    x_categorical = encode_categorical_features(
        categorical_features,
        cd_cleaned,
    )
    x = combine_features_with_encoded_categorical(x, x_categorical)
    x_train, x_test, y_train, y_test = split_data(x, y)
    rf_model = load_model(x_train, y_train)
    y_pred_rf = rf_model.predict(x_test)
    evaluate_model_mse(y_pred_rf, y_test)
    cd_cleaned["予測家賃_RF"] = rf_model.predict(x)
    save_to_csv(cd_cleaned)


if __name__ == "__main__":
    main()
