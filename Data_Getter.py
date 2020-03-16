"""
Gets data from Johns Hopkins GitHub repository:
    https://github.com/CSSEGISandData/COVID-19
"""
import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns


BASE_URL = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/"
#FILE_DIR = os.path.dirname(__file__)
FILE_DIR = "C:/Users/peter/Documents/Python Scripts/Outbreak_Mapping"

def get_table(url):
    """
    Gets data from url (csv) and converts to Pandas table
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


#def main():
now = datetime.today()
today = datetime(now.year, now.month, now.day)
fName = "Confirmed_" + (today-timedelta(days=1)).strftime("%m-%d-%y") + ".csv"
fPath = os.path.join(FILE_DIR, "timeseries_data", fName)
if not os.path.exists(fPath):
    # Get confirmed cases timeseries data
    confirmed_url = BASE_URL + "csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
    cases = get_table(confirmed_url)
    max_date = datetime.strptime(list(cases.columns)[-1], "%m/%d/%y")
    fName = "Confirmed_" + max_date.strftime("%m-%d-%y") + ".csv"
    print("Saving file:", fName)
    cases.to_csv(os.path.join(FILE_DIR, "timeseries_data", fName), sep=",", index=False)
else:
    print("Reading data:", fName)
    cases = pd.read_csv(fPath, sep=",", header=0)
print(cases.head())

us = cases[cases["Country/Region"] == "US"]
states = us[us.iloc[:,-1] != 0]

# Plot US states on map
sns.set(style="whitegrid", palette="pastel", color_codes=True)
sns.mpl.rc("figure", figsize=(10,6))


# if __name__ == "__main__":
#     main()
