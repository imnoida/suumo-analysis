# 必要なライブラリのインポート
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

import clean_data
import clean_outlier

# 説明変数と目的変数の選択
features = ["築年数", "構造", "階数", "面積", "徒歩"]
target = "家賃"

# データの前処理(外れ値のクリーニング)
cd = clean_data.clean_data()
cd_cleaned = clean_outlier.clean_outlier(cd)

# 説明変数と目的変数のデータを取得
X = cd_cleaned[features]
y = cd_cleaned[target]

# データの分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# モデルの構築
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)

# テストデータでの予測
y_pred_rf = rf_model.predict(X_test)

# モデルの評価
mse_rf = mean_squared_error(y_test, y_pred_rf)
print(f"Random Forest Mean Squared Error: {mse_rf}")

# 実際のデータに予測結果を結合
cd_cleaned["予測家賃_RF"] = np.nan  # 列を追加して初期化

# 予測結果を入れる列に予測値をセット
if "予測家賃_RF" in cd_cleaned.columns:
    cd_cleaned.loc[X_test.index, "予測家賃_RF"] = y_pred_rf
else:
    print("予測家賃_RF列が存在しません。")

# 予測結果を表示
result = cd_cleaned[["家賃", "予測家賃_RF"]].head()
