"""
This script gets the latest version of the assets/cases.csv file in 
 the repository:
    Virus (jakobzhao)

Data set cons:
    - Multiple patients per row

Data set pros:
    - Includes county data
"""

import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://github.com/jakobzhao/virus/blob/master/assets/cases.csv"
FILE_DIR = "c:/Users/peter/Documents/Python Scripts/Outbreak_Mapping"
# os.path.dirname(os.path.dirname(__file__))


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
    # return df


now = datetime.today()
today = datetime(now.year, now.month, now.day)
fName = "cases_" + (today-timedelta(days=1)).strftime("%m-%d-%y") + ".csv"
fPath = os.path.join(FILE_DIR, "case_data", fName)
#if not os.path.exists(fPath):
    # Get new timeseries data from API
#cases = get_table(URL)

html = requests.get(URL).text
soup = BeautifulSoup(html, features="html")
rows = soup.find_all("table")[0].find_all("tr")
# Extract header row
cols = rows[0].find_all("td")[1].get_text().split(",")
# Extract all data
data = [row.find_all("td")[1].get_text().replace('"', '').split(",") for row in rows[1:]]
df = pd.DataFrame(data, columns=cols)
df.head()
df.date = pd.to_datetime(df.date)
df.lng = df.lng.astype(float)
df.lat = df.lat.astype(float)
df.head()
df.dtypes
print(df.shape)


# max_date = datetime.strptime(list(cases.columns)[-1], "%m/%d/%y")
# fName = "cases_" + max_date.strftime("%m-%d-%y") + ".csv"
# print("Saving file:", fName)
# cases.to_csv(os.path.join(FILE_DIR, "timeseries_data", fName), sep=",", index=False)
# else:
#     print("Reading data:", fName)
#     cases = pd.read_csv(fPath, sep=",", header=0)

