# Scraping SEC for inside trading information

## Introduction
This project implements a web scraper for SEC website. 
For a given list of CIK, year, and month: Form4 is scrapped as XML and parsed to retrieve specific attributes.
Following attributes are scrapped and stored in CSV format:
- company
- issuer_trading_symbol
- report_date 
- securityTitle ( only 'Common Stock' is considered )
- shares_traded (This represents total number of shares Acquired, assuming that there could be multiple transactions)

## Tools used:

- Python 3.9
- Scrapy for web scraping
- Pandas for data analysis
- Plotly for interactive plots
- Streamlit for building dashboard

## Instructions to Run
1. set scraping parameters in `params.yml` file
2. Execute scraper: ` python -m scraper.main`. output is stored in `/data` directory in `csv` format
3. Open the interactive dashboard for data analysis using following command:
        `Streamlit run interface.py`
4. Open `http://localhost:8501` in your browser


## Output Screenshots
- Scrapped data is stored in data/Form4 folder. Following are the screenshots of how data look like:

![screenshot of /data/form4.csv file](https://github.com/ManpreetDhillon13/SecForm4Analysis/blob/134d0191ae384706bfc41eb6a8ef3fe360e17f70/img/form4_data.png)

- Following are the screenshots of developed Streamlit dashboard:

![screenshot of dashboard p1](https://github.com/ManpreetDhillon13/SecForm4Analysis/blob/134d0191ae384706bfc41eb6a8ef3fe360e17f70/img/streamlit_dashboard_1.png)

![screenshot of dashboard p2](https://github.com/ManpreetDhillon13/SecForm4Analysis/blob/134d0191ae384706bfc41eb6a8ef3fe360e17f70/img/streamlit_dashboard_2.png)