import clean_data
import clean_outlier
import display_plot
import model

if __name__ == "__main__":
    cd = clean_data.clean_data()
    filtered = clean_outlier.clean_outlier(cd)
    display_plot.average_rent_graph(filtered)
    display_plot.rent_hist(filtered)
    model.main()
