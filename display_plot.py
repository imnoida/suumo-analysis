import matplotlib.pyplot as plt

import clean_data

cd = clean_data.clean_data()
average_rent_per_city = cd.groupby("市")["家賃"].mean()
x = average_rent_per_city.index
y = average_rent_per_city.to_numpy()
plt.rcParams["font.family"] = "MS Gothic"
plt.figure(figsize=(15, 30))
plt.title("市ごとの平均家賃")
plt.xticks()
plt.yticks()
plt.xlabel("平均家賃")
plt.ylabel("市")
plt.grid()
plt.barh(x, y)
plt.show()
