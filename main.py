import clean_data
import display_plot

if __name__ == "__main__":
    cd = clean_data.clean_data()
    filtered = cd[
        (cd["家賃"] < 10)
    ]
    display_plot.average_rent_graph(filtered)
    display_plot.rent_hist(filtered)
