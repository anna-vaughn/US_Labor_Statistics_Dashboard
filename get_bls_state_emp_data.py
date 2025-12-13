import pandas as pd
import json
import requests
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

''' 
With mapping data (state/area codes):

SMS00000000000000001  = State and Area Employment, Hours, and Earnings
    (State code is pos 4-5)

* Seasonally adjusted *
'''
headers = {'Content-type': 'application/json'}
map_data = json.dumps({"seriesid": ['SMS01000000000000001',
                                'SMS02000000000000001',
                                'SMS04000000000000001',
                                'SMS05000000000000001',
                                'SMS06000000000000001',
                                'SMS08000000000000001',
                                'SMS09000000000000001',
                                'SMS10000000000000001',
                                'SMS12000000000000001',
                                'SMS13000000000000001',
                                'SMS15000000000000001',
                                'SMS16000000000000001',
                                'SMS17000000000000001',
                                'SMS18000000000000001',
                                'SMS19000000000000001',
                                'SMS20000000000000001',
                                'SMS21000000000000001',
                                'SMS22000000000000001',
                                'SMS23000000000000001',
                                'SMS24000000000000001',
                                'SMS25000000000000001',
                                'SMS26000000000000001',
                                'SMS27000000000000001',
                                'SMS28000000000000001',
                                'SMS29000000000000001',
                                'SMS30000000000000001',
                                'SMS31000000000000001',
                                'SMS32000000000000001',
                                'SMS33000000000000001',
                                'SMS34000000000000001',
                                'SMS35000000000000001',
                                'SMS36000000000000001',
                                'SMS37000000000000001',
                                'SMS38000000000000001',
                                'SMS39000000000000001',
                                'SMS40000000000000001',
                                'SMS41000000000000001',
                                'SMS42000000000000001',
                                'SMS44000000000000001',
                                'SMS45000000000000001',
                                'SMS46000000000000001',
                                'SMS47000000000000001',
                                'SMS48000000000000001',
                                'SMS49000000000000001',
                                'SMS50000000000000001',
                                'SMS51000000000000001',
                                'SMS53000000000000001',
                                'SMS54000000000000001',
                                'SMS55000000000000001',
                                'SMS56000000000000001'], 
                    "startyear":prevyear, "endyear":curryear, "calculations":"true", "annualaverage":"true", "registrationkey":api_key})
m_p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=map_data, headers=headers)
m_json_data = json.loads(m_p.text)

# Create empty list to add relevent values to.
m_x = []

# Loop through data.
for series in m_json_data['Results']['series']:
    seriesId = series['seriesID']
    
    # Iterate through 'data' dictionary and store values.
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
            # Add values to list x_row.
            x_row = [seriesId, year, period, month, value, footnotes[0:-1]]

            # Iterate through net and pct changes dictionary to grab values and append.
            for mochange, val in net_changes.items():
                x_row.append(val)
            for mochange, val in pct_changes.items():
                x_row.append(val)
            
            # Add values to list x.
            m_x.append(x_row)

# Convert list to dataframe for easier analysis.
m_x = pd.DataFrame(m_x)

# Rename columns.
alldat = m_x.rename(columns={0:'seriesID', 1:'year', 2:'period', 3:'month', 4:'value', 5:'footnotes', 6:'netchg_1mo', 7:'netchg_3mo', 8:'netchg_6mo', 9:'netchg_12mo', 10:'pctchg_1mo', 11:'pctchg_3mo', 12:'pctchg_6mo', 13:'pctchg_12mo'})

''' Clean data and prep for analysis for dashboard! '''
# Create a new column time_period for filtering purposes.
alldat['time_period'] = alldat[['month', 'year']].apply(lambda x: ', '.join(x.astype(str).values), axis=1)
# Convert back to a date format.
alldat['time_period'] = pd.to_datetime(alldat['time_period'], format = '%B, %Y')

# Create function to pair the seriesIDs with their names.
def sname(row):
    if row['seriesID'] == 'SMS01000000000000001': 
        val = 'AL'
    elif row['seriesID'] == 'SMS02000000000000001': 
        val = 'AK'
    elif row['seriesID'] == 'SMS04000000000000001': 
        val = 'AZ'
    elif row['seriesID'] == 'SMS05000000000000001': 
        val = 'AR'
    elif row['seriesID'] == 'SMS06000000000000001': 
        val = 'CA'
    elif row['seriesID'] == 'SMS08000000000000001': 
        val = 'CO'
    elif row['seriesID'] == 'SMS09000000000000001': 
        val = 'CT'
    elif row['seriesID'] == 'SMS10000000000000001': 
        val = 'DE'
    elif row['seriesID'] == 'SMS11000000000000001': 
        val = 'DC'
    elif row['seriesID'] == 'SMS12000000000000001': 
        val = 'FL'
    elif row['seriesID'] == 'SMS13000000000000001': 
        val = 'GA'
    elif row['seriesID'] == 'SMS15000000000000001': 
        val = 'HI'
    elif row['seriesID'] == 'SMS16000000000000001': 
        val = 'ID'
    elif row['seriesID'] == 'SMS17000000000000001': 
        val = 'IL'
    elif row['seriesID'] == 'SMS18000000000000001': 
        val = 'IN'
    elif row['seriesID'] == 'SMS19000000000000001': 
        val = 'IA'
    elif row['seriesID'] == 'SMS20000000000000001': 
        val = 'KS'
    elif row['seriesID'] == 'SMS21000000000000001': 
        val = 'KY'
    elif row['seriesID'] == 'SMS22000000000000001': 
        val = 'LA'
    elif row['seriesID'] == 'SMS23000000000000001': 
        val = 'ME'
    elif row['seriesID'] == 'SMS24000000000000001': 
        val = 'MD'
    elif row['seriesID'] == 'SMS25000000000000001': 
        val = 'MA'
    elif row['seriesID'] == 'SMS26000000000000001': 
        val = 'MI'
    elif row['seriesID'] == 'SMS27000000000000001': 
        val = 'MN'
    elif row['seriesID'] == 'SMS28000000000000001': 
        val = 'MS'
    elif row['seriesID'] == 'SMS29000000000000001': 
        val = 'MO'
    elif row['seriesID'] == 'SMS30000000000000001': 
        val = 'MT'
    elif row['seriesID'] == 'SMS31000000000000001': 
        val = 'NE'
    elif row['seriesID'] == 'SMS32000000000000001': 
        val = 'NV'
    elif row['seriesID'] == 'SMS33000000000000001': 
        val = 'NH'
    elif row['seriesID'] == 'SMS34000000000000001': 
        val = 'NJ'
    elif row['seriesID'] == 'SMS35000000000000001': 
        val = 'NM'
    elif row['seriesID'] == 'SMS36000000000000001': 
        val = 'NY'
    elif row['seriesID'] == 'SMS37000000000000001': 
        val = 'NC'
    elif row['seriesID'] == 'SMS38000000000000001': 
        val = 'ND'
    elif row['seriesID'] == 'SMS39000000000000001': 
        val = 'OH'
    elif row['seriesID'] == 'SMS40000000000000001': 
        val = 'OK'
    elif row['seriesID'] == 'SMS41000000000000001': 
        val = 'OR'
    elif row['seriesID'] == 'SMS42000000000000001': 
        val = 'PA'
    elif row['seriesID'] == 'SMS44000000000000001': 
        val = 'RI'
    elif row['seriesID'] == 'SMS45000000000000001': 
        val = 'SC'
    elif row['seriesID'] == 'SMS46000000000000001': 
        val = 'SD'
    elif row['seriesID'] == 'SMS47000000000000001': 
        val = 'TN'
    elif row['seriesID'] == 'SMS48000000000000001': 
        val = 'TX'
    elif row['seriesID'] == 'SMS49000000000000001': 
        val = 'UT'
    elif row['seriesID'] == 'SMS50000000000000001': 
        val = 'VT'
    elif row['seriesID'] == 'SMS51000000000000001': 
        val = 'VA'
    elif row['seriesID'] == 'SMS53000000000000001': 
        val = 'WA'
    elif row['seriesID'] == 'SMS54000000000000001': 
        val = 'WV'
    elif row['seriesID'] == 'SMS55000000000000001': 
        val = 'WI'
    else: 
        val = 'WY'

    return val

# Create a new column series_name using the above funtion.
alldat['series_name'] = alldat.apply(sname, axis=1)

# Save the data to a csv file.
alldat.to_csv('bls_all_emp_data.csv')