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

- Python
- Scrapy framework
- Pandas for data analysis
- Streamlit for user interface

## Instructions to Run
1. set scraping parameters in `params.yml` file
2. Execute scraper: ` python -m scraper.main`. output is stored in `/data` directory in `csv` format
3. Open the interactive dashboard for data analysis using following command:
        `Streamlit run interface.py`
4. Open `http://localhost:8501` in your browser


## Output Screenshots
- Scrapped data is stored in data/Form4 folder. Following are the screenshots of how data look like:

- [ADD SCREENSHOTS HERE]