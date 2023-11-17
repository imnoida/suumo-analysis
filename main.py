import clean_data
import display_plot

if __name__ == "__main__":
    cd = clean_data.clean_data()
    filtered = cd[
        (cd["カテゴリー"] == "賃貸アパート")
        & (cd["築年数"] < 10)
        & (cd["家賃"] < 10)
    ]
    display_plot.display_plot(filtered)
