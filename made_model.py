# 必要なライブラリのインポート
from logging import Logger

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

import clean_data
import clean_outlier
from logger import set_logger

log: Logger = set_logger(module_name=__name__)
# 説明変数と目的変数の選択
features = ["築年数", "構造", "階数", "面積", "徒歩"]
target = "家賃"
categorical_features = ["地域", "駅", "沿線"]

# データの前処理(外れ値のクリーニング)
cd = clean_data.clean_data()
cd_cleaned = clean_outlier.clean_outlier(cd)

# 説明変数と目的変数のデータを取得
X = cd_cleaned[features]
y = cd_cleaned[target]

# カテゴリカル変数のエンコーディング
encoder = OneHotEncoder()
X_categorical = encoder.fit_transform(cd_cleaned[categorical_features]).toarray()

# エンコードされたカテゴリカル変数を結合
X = np.concatenate((X.to_numpy(), X_categorical), axis=1)

# 説明変数のリストを更新
features += encoder.get_feature_names_out(categorical_features).tolist()

# データの分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42,
)

# モデルの構築
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)

# テストデータでの予測
y_pred_rf = rf_model.predict(X_test)

# モデルの評価
mse_rf = mean_squared_error(y_test, y_pred_rf)
log.info("ランダムフォレストの平均二乗誤差: %s", mse_rf)

# 実際のデータに予測結果を結合
cd_cleaned["予測家賃_RF"] = rf_model.predict(X)

# 予測結果を表示
result = cd_cleaned[["家賃", "予測家賃_RF"]]
