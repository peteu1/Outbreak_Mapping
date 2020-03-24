"""
This script gets the latest data from the repository:
    nCoV2019 (beoutbreakprepared)
Latest data corresponds to newest file in:
    dataset_archive/outside_Hubei_<data/time>.data

Data set cons:
    - Only has a small fraction of actual cases

Data set pros:
    - One patient per row
    - Patient details to run statistical analysis
    - Includes county/lat/long
"""
import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd

# Location to save outputs
FILE_DIR = "c:/Users/peter/Documents/Python Scripts/Outbreak_Mapping"
OUT_DIR = os.path.join(FILE_DIR, "case_data")
# os.path.dirname(os.path.dirname(__file__))

# URL to get list of files
REPO_URL = "https://github.com/beoutbreakprepared/nCoV2019/blob/master/dataset_archive/"
# URL to request data from
REQ_URL = "https://raw.githubusercontent.com/beoutbreakprepared/nCoV2019/master/dataset_archive/"


def get_data(fName):
    url = REQ_URL + fName
    print("Reading:", url)
    df = pd.read_csv(url, index_col=0)
    return df

## Main
# TODO: Get file name automatically from list of files
fName = "outside_Hubei.data.19032020T011105.csv"
df = get_data(fName)
df.head()
df.shape
df.columns

# Extract US data, select columns
us = df[df.country == "United States"]
new_cols = list(df.columns)
# Remove columns with little data
remove_cols = [
    "wuhan(0)_not_wuhan(1)",
    "date_onset_symptoms", 
    "date_admission_hospital", 
    "lives_in_Wuhan", 
    "symptoms",
    "reported_market_exposure",
    "chronic_disease_binary",
    "chronic_disease", 
    "source",
    "sequence_available",
    "notes_for_discussion",
    "admin1",
    "admin2",
    "admin3",
    "country_new",
    "admin_id",
    "data_moderator_initials",
    "location"
]
for c in remove_cols:
    new_cols.remove(c)
us = us[new_cols]
(~us.isna()).sum()

us.head()
us.travel_history_location[-15:]
