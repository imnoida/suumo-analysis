import matplotlib.pyplot as plt
import clean_data

cd = clean_data.clean_data().head(100)
x = cd["市"]
y = cd["家賃"]
font = "MS Gothic"
plt.xticks(fontname=font)
plt.yticks(fontname=font)
plt.xlabel("市", fontname=font)
plt.ylabel("平均家賃", fontname=font)
plt.grid()
plt.bar(x, y)
plt.show()
