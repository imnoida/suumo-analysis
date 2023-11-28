import clean_data
import display_plot
import clean_outlier

if __name__ == "__main__":
    cd = clean_data.clean_data()
    co = clean_outlier.clean_outlier(cd)
    display_plot.average_rent_graph(cd)
    filtered = co
    display_plot.rent_hist(filtered)
