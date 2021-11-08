"""
Rhys Broughton - 710043307 - 03/11/2021
CA for ECM1400

"""


from covid_data_handler import parse_csv_data, process_csv_data, covid_API_request
from covid_news_handling import news_API_request
from uk_covid19 import Cov19API
import flask


def test_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639
    print(data)


def test_csv_handling():
    data = process_csv_data(parse_csv_data('nation_2021-10-28.csv'))
    print(data)


def test_covid_request():
    data = covid_API_request()

def test_news_request():
    data = news_API_request()



test_news_request()