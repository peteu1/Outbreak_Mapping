"""
Gets data from Johns Hopkins GitHub repository:
    https://github.com/CSSEGISandData/COVID-19


Data set cons:
    - No county data, just US state/world country

Data set pros:
    - Most complete dataset
"""
import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd


BASE_URL = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/"
FILE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_table(url):
    """
    Gets data from url (csv) and converts to Pandas table

    Args:
        url (str): URL to dataset (csv) in GitHub

    Returns:
        df (pandas.dataframe): the data from GitHub formatted as a dataframe
    """
    print("Reading:", url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html")
    rows = soup.find_all("table")[0].find_all("tr")
    # Extract header row
    cols = []
    for col_name in rows[0].find_all("th"):
        cols.append(col_name.get_text())
    # Extract all data
    data = []
    for row in rows[1:]:
        row_data = [td.text for td in row.find_all("td")]
        data.append(row_data[1:])
    # Assemble dataframe
    df = pd.DataFrame(data, columns=cols)
    print(df.shape)
    return df


def get_timeseries_data(kwd):
    """
    Gets the specified time-series dataset from the GitHub API if new
     data available, otherwise reads current saved dataset.
    
    Args:
        kwd (str): Keyword (either "Confirmed", "Deaths", or "Recovered")
    """
    now = datetime.today()
    today = datetime(now.year, now.month, now.day)
    fName = kwd + "_" + (today-timedelta(days=1)).strftime("%m-%d-%y") + ".csv"
    fPath = os.path.join(FILE_DIR, "timeseries_data", fName)
    if not os.path.exists(fPath):
        # Get new timeseries data from API
        API_url = BASE_URL + f"csse_covid_19_time_series/time_series_19-covid-{kwd}.csv"
        cases = get_table(API_url)
        max_date = datetime.strptime(list(cases.columns)[-1], "%m/%d/%y")
        fName = kwd + "_" + max_date.strftime("%m-%d-%y") + ".csv"
        print("Saving file:", fName)
        cases.to_csv(fPath, sep=",", index=False)
    else:
        print("Reading data:", fName)
        cases = pd.read_csv(fPath, sep=",", header=0)
    return cases


def get_confirmed():
    """
    Returns:
        cases (pandas.dataframe): The updated dataset for confirmed cases
    """
    return get_timeseries_data("Confirmed")


def get_recovered():
    """
    Returns:
        cases (pandas.dataframe): The updated dataset for recovered cases
    """
    return get_timeseries_data("Recovered")


def get_deaths():
    """
    Returns:
        cases (pandas.dataframe): The updated dataset for deaths
    """
    return get_timeseries_data("Deaths")


get_confirmed()