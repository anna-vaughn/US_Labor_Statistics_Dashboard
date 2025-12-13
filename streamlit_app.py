import streamlit as st
import pandas as pd

# Set to wide layout to make the most of the browser screen.
st.set_page_config(layout='wide')

st.title('Job Market Overview (US Labor Statistics)')

# Import data.
data = pd.read_csv('bls_data.csv', index_col = 0)

# Create sidebar for the filters.
with st.sidebar.form('filter_form'):
    st.header("Filters")
    st.write("Use this to filter the dashboard display.")
    
    st.subheader('Series')

    st.subheader('Timeframe')
    #year = st.sidebar

    st.subheader('Variables to display')

    submit = st.form_submit_button('Apply')
    #if submit:

# Columns displaying the current month data for each series along the top of the dashbaord.
## Create df containing data of most recent month for each series.
recentmo = data.loc[(data.groupby('seriesID')['time_period'].idxmax())]

# Create variables for each series.
## All Employees
recentNFE = recentmo.loc[(recentmo['seriesID'] == 'CES0000000001')]
## Unemployment rates
recentUR = recentmo.loc[(recentmo['seriesID'] == 'LNS14000000')]
## Job openings rate
recentJO = recentmo.loc[(recentmo['seriesID'] == 'JTS000000000000000JOR')]
## Hires rate
recentHR = recentmo.loc[(recentmo['seriesID'] == 'JTS000000000000000HIR')]
## Quits rate
recentQR = recentmo.loc[(recentmo['seriesID'] == 'JTS000000000000000QUR')]
## Layoffs and discharges rate
recentLDR = recentmo.loc[(recentmo['seriesID'] == 'JTS000000000000000LDR')]

# Current month (by default but can be filtered) data for each series along the top of the page.
## Add the number of columns to the dashboard.
s1, s2, s3, s4, s5, s6 = st.columns(6)
## Add values to each column.
s1.metric('All Non-Farm Employees (Thousands)', recentNFE['value'])
s2.metric('Unemployment Rate', recentUR['value'])
s3.metric('Job Openings and Labor Turnover Rate', recentJO['value'])
s4.metric('Hires Rate', recentHR['value'])
s5.metric('Quits Rate', recentQR['value'])
s6.metric('Layoffs And Discharges Rate', recentLDR['value'])

# Create two tabs, one for each visualization
t1, t2 = st.tabs(['Line Chart', 'Map'])

# Prep data for line chart.
## Group series with common data types together.
nfemp = data.loc[(data['seriesID'] == 'CES0000000001')]
rates = data.loc[(data['seriesID'] != 'CES0000000001')]

with t1:
    st.header('Line Chart Here.')
    
    # Create columns to display the two graphs side-by-side.
    emp, rate = st.columns(2)
    # Display All Employees Data.
    emp.line_chart(nfemp, x='time_period', y='value', color='series_name')

    rate.line_chart(rates, x='time_period', y='value', color='series_name')

with t2:
    st.header('Eventually a map will go here.')

# Line chart(s) for easy comparisons over time.
## Allow viewer to add/change variables.
## Allow viewer to view data points when hovering or clicking.
## Allow viewer to download data.


# Map of U.S. for state-by-state comparison.
## Allow viewer to add/change variables.
## Allow viewer to view data points when hovering or clicking.
## Allow viewer to download data.



# Show data in streamlit dashboard.
st.dataframe(data)
st.dataframe(recentmo)
