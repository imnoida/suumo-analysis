from bs4 import BeautifulSoup
import requests

target_url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=050&bs=040&ta=23&sc=23101&sc=23102&sc=23103&sc=23104&sc=23105&sc=23106&sc=23107&sc=23108&sc=23109&sc=23110&sc=23111&sc=23112&sc=23113&sc=23114&sc=23115&sc=23116&sc=23201&sc=23202&sc=23203&sc=23204&sc=23205&sc=23206&sc=23207&sc=23208&sc=23209&sc=23210&sc=23211&sc=23212&sc=23213&sc=23214&sc=23215&sc=23216&sc=23217&sc=23219&sc=23220&sc=23221&sc=23222&sc=23223&sc=23224&sc=23225&sc=23226&sc=23227&sc=23228&sc=23229&sc=23230&sc=23231&sc=23232&sc=23233&sc=23234&sc=23235&sc=23236&sc=23237&sc=23238&sc=23302&sc=23340&sc=23360&sc=23420&sc=23440&sc=23500&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=25&pc=50&page={}"


def request_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_max_page():
    element = request_html(target_url.format(1))
    max_page = element.select(
        "#js-leftColumnForm > div.pagination_set > div.pagination.pagination_set-nav > ol > li:nth-of-type(13) > a")
    return max_page


print(get_max_page())
