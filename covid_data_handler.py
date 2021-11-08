"""
Rhys Broughton - 710043307 - 03/11/2021
CA for ECM1400
This file is for the handeling of all covid data, it will interface with the CSV file, the Cov19API, and the covid new API

"""
import csv
from uk_covid19 import Cov19API
import json


def reformat(ele):
    # gets rid of the extra chars
    eleNoApp = [s.replace("'", "") for s in ele]
    eleNoBrakFront = [s.replace("[", "") for s in eleNoApp]
    ele = [s.replace("]", "") for s in eleNoBrakFront]

    return ele


def parse_csv_data(csv_filename):
    # this func returns the csv data as a list of strings
    with open(csv_filename, newline='') as csv_file:
        data = csv.reader(csv_file, delimiter=' ', quotechar='|')
        list_of_data = []
        for row in data:
            list_of_data.append(row)
        return list_of_data


def process_csv_data(covid_csv_data):
    # this func processes the data and gives cases in the last 7 days, current hospital admissions, total death

    # this gets the current hospital cases from the most recent item in the CSV file
    i = 0
    element1 = str(covid_csv_data[1]).split(",")
    hospital_cases = element1[5]
    print(hospital_cases)

    # this gets the total deaths
    while True:
        i += 1
        # turns the element into its own list
        ele = str(covid_csv_data[i]).split(",")

        # find the first value in the deaths column that isn't NULL data
        if ele[4] != "":
            deaths = ele[4]
            break

    print(deaths)

    # this gets the total number of cases in the last seven days
    total_cases_7days = 0
    for i in range(6):
        # turns the element into its own list
        ele_no_format = str(covid_csv_data[i + 1]).split(",")
        # gets rid of the extra brackets and commas in the values
        ele = reformat(ele_no_format)
        # checks that the element has a value in it, so to count the last 7 days excluding the day before code ran
        # where is incomplete
        if ele[6] != '':
            total_cases_7days += int(ele[6])

    print(total_cases_7days)

    # outputs the values needed
    return total_cases_7days, hospital_cases, deaths


def get_needed_JSON_data(data_in_list, needed_VAR):
    i = 0
    # get newCasesByPublishDate
    while True:
        json_data_to_be_format = data_in_list[i]
        if str(json_data_to_be_format[needed_VAR]) != "None":
            current_data = json_data_to_be_format[needed_VAR]
            break
        i += 1
    return current_data


def covid_API_request(location='Exeter', location_type='ltla'):
    # this func handles the live data access from the covid API

    # tells program where is needs to get the data for
    filter_for_location = [
        f'areaType={location_type}',
        f'areaName={location}'
    ]

    # creates a dictionary for the data
    struc_Dictionary = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
        "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate"
    }

    # instantiation
    api = Cov19API(filters=filter_for_location,
                   structure=struc_Dictionary)

    # formating the data
    # here i will be extracing this most up-to date data for each collum

    data_Extracted = api.get_json()

    data_in_list = data_Extracted["data"]

    output_dictionary = {

        "newCasesByPublishDate": get_needed_JSON_data(data_in_list, "newCasesByPublishDate"),
        "cumCasesByPublishDate": get_needed_JSON_data(data_in_list, "cumCasesByPublishDate"),
        "newDeaths28DaysByDeathDate": get_needed_JSON_data(data_in_list, "newDeaths28DaysByDeathDate"),
        "cumDeaths28DaysByDeathDate": get_needed_JSON_data(data_in_list, "cumDeaths28DaysByDeathDate")

    }
    print(output_dictionary)
    return output_dictionary

def schedule_covid_updates(update_interval, update_name):
    print("update covid data")
