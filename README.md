# US_Labor_Statistics_Dashboard
ECON 8320 Semester Project

This project uses Python to get data from the BLS Public Data API (specifically v2.0, please don't use my API key for malicious reasons!) and creates a Streamlit dashboard with visualizations that give insight into the current job market.

## How it's made
This was made with 7 series. The first 6 were straightforward API calls. I used the API v2.0 to get the net and percent changes MoM, which were helpful in visualizing the changes in data. 
CES0000000001         = Non-farm workers
LNS14000000           = Unemployment rates
JTS000000000000000JOR = Job openings rate
JTS000000000000000HIR = Hires rate
JTS000000000000000QUR = Quits rate
JTS000000000000000LDR = Layoffs and discharges rate

The last series was more difficult to obtain. I had wanted to create a map of the U.S. for all of the above series', however after looking through BLS's Series ID Formats (https://www.bls.gov/help/hlpforma.htm) and finding the assiciated Series IDs not all of them had data for all 50 states. Although I was dissapointed, I was able to get data for all 50 states for the number of employees by state. The series format I used here was - 
SMS01000000000000001
- where I changed the 4th and 5th position to the specific state code I wanted to get (x 49!).

## View my dashboard!
Link to my dashboard: https://uslaborstatisticsdashboard-waupbpr2urzp6cdnzemb65.streamlit.app/

Read more about the BLS Public Data API here: https://www.bls.gov/developers/home.htm
