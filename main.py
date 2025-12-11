import pandas as pd
import json
#import plotly.express as px
import requests
#import streamlit as st
from datetime import datetime

'''Ensure a rolling 12 mo of data is available.'''
# Save current year and previous year as a variable.
curryear = datetime.today().year
prevyear = curryear - 1
# Save current month as a variable.
currmo = datetime.today().strftime("%B")
# Save month from 12 months ago as a variable.
## Subtracting dates is hard! First must save current datetime.
## Then we can use pandas DateOffset class to get the datetime from 12 months ago.
## Then we save that month as the name (string) so we can find it in the API.
currdate = datetime.today()
rollingdate = currdate - pd.DateOffset(months=12)
rollingmo = rollingdate.strftime("%B")

# Call API Registration Key to use version 2.0.
with open('API_KEY.txt', 'r') as file:
    api_key = file.read().strip()

# Code below is based off of https://www.bls.gov/developers/api_python.htm#python2 with modifications.
''' 
CES0000000001         = Non-farm workers
LNS14000000           = Unemployment rates
JTS000000000000000JOR = Job openings rate
JTS000000000000000HIR = Hires rate
JTS000000000000000QUR = Quits rate
JTS000000000000000LDR = Layoffs and discharges rate
* All series seasonally adjusted *
'''
headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['CES0000000001','LNS14000000', 'JTS000000000000000JOR', 'JTS000000000000000HIR', 'JTS000000000000000QUR', 'JTS000000000000000LDR'], "startyear":prevyear, "endyear":curryear, "calculations":"true", "annualaverage":"true", "registrationkey":api_key})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)

# Create empty list to add relevent values to.
x = []

# Loop through data.
for series in json_data['Results']['series']:
    seriesId = series['seriesID']
    
    for item in series['data']:
        year = item['year']
        period = item['period']
        month = item['periodName']
        value = item['value']
        footnotes=""
        for footnote in item['footnotes']:
            if footnote:
                footnotes = footnotes + footnote['text'] + ','
        calcs = item.get('calculations', {})
        net_changes = calcs.get('net_changes', {})
        pct_changes = calcs.get('pct_changes', {})

        # This grabs all 12 months (if available) of data for each year.
        if 'M01' <= period <= 'M12':
            x_row = [seriesId, year, period, month, value, footnotes[0:-1]]

            # Iterate through net and pct changes dictionary to grab values and append.
            for mochange, val in net_changes.items():
                x_row.append(val)
            for mochange, val in pct_changes.items():
                x_row.append(val)
            
            x.append(x_row)
            
# Convert list to dataframe for easier analysis.
x = pd.DataFrame(x)

# Rename columns.
alldat = x.rename(columns={0:'seriesID', 1:'year', 2:'period', 3:'month', 4:'value', 5:'footnotes', 6:'netchg_1mo', 7:'netchg_3mo', 8:'netchg_6mo', 9:'netchg_12mo', 10:'pctchg_1mo', 11:'pctchg_3mo', 12:'pctchg_6mo', 13:'pctchg_12mo'})

print(alldat)