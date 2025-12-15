import streamlit as st
import pandas as pd
import plotly.express as px

# Give the tab a name, and set to wide layout to make the most of the browser screen.
st.set_page_config(page_title='Job Market Overview', layout='wide')

# Info about the dashboard:
st.title('Job Market Overview (US Labor Statistics)')
st.write('This data was obtained using the BLS Public Data API (v2.0). All data used in this dashboard is seasonally adjusted.')
st.page_link(page='https://www.bls.gov/developers/home.htm', label='About BLS Public Data API', icon=':material/open_in_new:')
st.page_link(page='https://www.bls.gov/help/def/sm.htm#seasonally', label='BLS Seasonal Adjustment Explanation', icon=':material/open_in_new:')

# Import data. index_col is required here because the files already have an index col.
data = pd.read_csv('./data/bls_data.csv', index_col = 0)
map_data = pd.read_csv('./data/bls_state_emp_data.csv', index_col = 0)

# Create sidebar to display the filters.
with st.sidebar.form('filter_form'):
    st.header('Select filters, then click "Apply". Refresh to reset the filters.')

    # Allow change to value displayed.
    displayvar = ['value', 'netchg_1mo', 'netchg_3mo', 'netchg_6mo', 'netchg_12mo', 'pctchg_1mo', 'pctchg_3mo', 'pctchg_6mo', 'pctchg_12mo']
    filter_var = st.pills('Select Variable To Display In Dashboard', displayvar, selection_mode='single', default='value')
    
    # Allow selection on a monthly basis for metrics.
    filter_mo = st.selectbox('Select Month To Display In Metrics', data['time_period'])

    # Allow filtering on series.
    series = data['series_name'].unique().tolist()
    filter_series = st.multiselect('Select Series To Display In Line Chart(s)', series, default=['All Employees', 'Unemployment Rate', 'Job Openings and Labor Turnover Rate', 'Hires Rate', 'Quits Rate', 'Layoffs and Discharges Rate'])

    # Reformat time_period so it can be used in the slider filtering.
    data['time_period'] = pd.to_datetime(data['time_period'])
    mintime = data['time_period'].min().to_pydatetime()
    maxtime = data['time_period'].max().to_pydatetime()
    # Get rolling 12 months of data to automatically display on the filter.
    rolling12mo = maxtime - pd.DateOffset(months=12)
    rolling12mo = rolling12mo.to_pydatetime()
    filter_time = st.slider('Select Timeframe For Line Chart(s)', min_value=mintime, max_value=maxtime, value=(rolling12mo, maxtime), format='YYYY-MM')

    # Allow selection on a monthly basis for the map.
    filter_mo_map = st.selectbox('Select Month To Display In Map', map_data['time_period'])

    submit = st.form_submit_button('Apply')

# Columns displaying the current month data for each series along the top of the dashbaord.
s1, s2, s3, s4, s5, s6 = st.columns(6)

## Create df containing data of selected month for each series.
selectedmo = data.loc[(data['time_period'] == filter_mo)]

## Create variables for each series.
### All Employees
recentNFE = selectedmo.loc[(selectedmo['seriesID'] == 'CES0000000001')]
## Unemployment rates
recentUR = selectedmo.loc[(selectedmo['seriesID'] == 'LNS14000000')]
## Job openings rate
recentJO = selectedmo.loc[(selectedmo['seriesID'] == 'JTS000000000000000JOR')]
## Hires rate
recentHR = selectedmo.loc[(selectedmo['seriesID'] == 'JTS000000000000000HIR')]
## Quits rate
recentQR = selectedmo.loc[(selectedmo['seriesID'] == 'JTS000000000000000QUR')]
## Layoffs and discharges rate
recentLDR = selectedmo.loc[(selectedmo['seriesID'] == 'JTS000000000000000LDR')]

## Add values to each column based on variable selected in filters.
## If variable selected is value display the deltas. 
if filter_var == 'value':
    s1.metric('All Non-Farm Employees', recentNFE['value'], delta=recentNFE.iloc[0]['netchg_1mo'])
    s2.metric('Unemployment Rate', recentUR['value'], delta=recentUR.iloc[0]['pctchg_1mo'], delta_color='inverse')
    s3.metric('Job Openings and Labor Turnover Rate', recentJO['value'], delta=recentJO.iloc[0]['pctchg_1mo'])
    s4.metric('Hires Rate', recentHR['value'], delta=recentHR.iloc[0]['pctchg_1mo'])
    s5.metric('Quits Rate', recentQR['value'], delta=recentQR.iloc[0]['pctchg_1mo'],delta_color='inverse')
    s6.metric('Layoffs And Discharges Rate', recentLDR['value'], delta=recentLDR.iloc[0]['pctchg_1mo'], delta_color='inverse')

else:
    s1.metric('All Non-Farm Employees', recentNFE[filter_var])
    s2.metric('Unemployment Rate', recentUR[filter_var])
    s3.metric('Job Openings and Labor Turnover Rate', recentJO[filter_var])
    s4.metric('Hires Rate', recentHR[filter_var])
    s5.metric('Quits Rate', recentQR[filter_var])
    s6.metric('Layoffs And Discharges Rate', recentLDR[filter_var])

# Create two tabs, one for each visualization
t1, t2 = st.tabs(['Line Chart', 'Map'])

# Prep data for line chart.
## Force the Timeframe filter to always default to the 1st of each month so it's included in the display.
start = filter_time[0].replace(day=1)
end = filter_time[1].replace(day=1)
## Create variable to store filtered values which will be used to make line charts dynamic.
series_filtered = data[(data['series_name'].isin(filter_series)) & (data['time_period'].between(start, end))]

with t1:  
    if 'All Employees' in filter_series:
        ## Group series with common data types together.
        nfemp = series_filtered.loc[series_filtered['seriesID'] == 'CES0000000001']
        rates = series_filtered.loc[series_filtered['seriesID'] != 'CES0000000001']

        # Create columns to display the two graphs side-by-side.
        emp, rate = st.columns(2)

        # Display All Employees Data.
        allemp = px.line(nfemp, x='time_period', y=filter_var, color='series_name')
        ## Show legend on bottom of graph.
        allemp.update_layout(legend=dict(orientation='h'))
        ## Show plot.
        emp.plotly_chart(allemp)
        
        # Display dataframe data.
        emp.dataframe(nfemp)
        
        # Display all other data (Rate/%)
        rates_chart = px.line(rates, x='time_period', y=filter_var, color='series_name')
        ## Show legend on bottom of graph.
        rates_chart.update_layout(legend=dict(orientation='h'))
        ## Show plot.
        rate.plotly_chart(rates_chart)
        
        # Display dataframe data.
        rate.dataframe(rates)
    else:
        # When data doesn't include all employees, display only one chart in the tab.
        dat_chart = px.line(series_filtered, x='time_period', y=filter_var, color='series_name')
        ## Show legend on bottom of graph.
        dat_chart.update_layout(legend=dict(orientation='h'))
        ## Show plot.
        st.plotly_chart(dat_chart)
        
        # Display dataframe of data.
        st.dataframe(series_filtered)


# Prep data for map.
## Create df containing data of selected month for map.
map_selectedmo = map_data.loc[(map_data['time_period'] == filter_mo_map)]
## Create map using plotly.
fig = px.choropleth(data_frame=map_selectedmo , locations='series_name', locationmode='USA-states', color=filter_var, scope='usa')

with t2:
    st.header('All employees by state, in thousands.')
    st.write('Automatically displaying most recent month of data. Use the filters to the left to change the month displayed.')
    st.page_link(page='https://www.bls.gov/help/hlpforma.htm#SM', label='BLS API SeriesID This Data is Based Off', icon=':material/open_in_new:')
    st.plotly_chart(fig, theme=None)
    st.dataframe(map_selectedmo)