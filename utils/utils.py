from __future__ import annotations
import yaml
import pandas as pd
import datetime
# helper functions for scraper
def read_params(params_file:str):
    with open(params_file, 'r') as fhandle:
        return yaml.safe_load(fhandle)
    
def split_date(date_obj:datetime)->tuple[str,str,str]:
    """ 
    helper function to parse date
    """
    return date_obj.year, date_obj.month, date_obj.day

def preprocess_table(submission_table:pd.DataFrame)->pd.DataFrame:
    """
    converts string formatted date to datetime format and
    splits date into year, month, day to facilitate futher filtrations
    """
    submission_table.drop(columns=['Size'], inplace=True)
    submission_table.rename(columns={'Last Modified':'lastModified'}, inplace=True)
    submission_table['lastModified'] = pd.to_datetime(submission_table['lastModified'])
    submission_table[['year', 'month', 'day']]  =  submission_table.apply(
        lambda row: split_date(row.lastModified),
        axis='columns', 
        result_type= 'expand')
    return submission_table

def filter_folder_name(submission_table:pd.DataFrame, year:list, month:list)->pd.DataFrame:
    """
    for a given year, month or day - this function filters name of the submission
    folders which will be used further by scrapper for checking form4 submissions 
    """
    subset = submission_table[(submission_table['year'].isin(year)) & (submission_table['month'].isin(month))]
    return list(subset['Name'])

# helper functions for interface.py
def get_hist_data(dataset:pd.DataFrame, company_codes:list[str])->tuple[list[pd.Series], list[str]]:
    hist_data = []
    for company in company_codes:
        dist = dataset[dataset['issuer_trading_symbol'] == company]['shares_traded']
        hist_data.append(dist)
    group_labels = get_group_labels(company_codes)
    return hist_data, group_labels


def formatted_company_label(cik:str)->str:
    company_cik = {
        'AAPL': 'Apple',
        'TSLA':'Tesla',
        'MSFT':'Microsoft',
        'GOOGL': 'Google'
    }
    return company_cik[cik]

def get_group_labels(company_codes:list[str])->list[str]:
    group_labels = [formatted_company_label(code) for code in company_codes]
    return group_labels

def get_total_trades(dataset:pd.DataFrame, companies:list[str]):
    totals = []
    for company in companies:
        total = sum(dataset[dataset['issuerTradingSymbol'] == company]['sharesTraded'])
        totals.append(total)
        print(f"{company}:{total}")
    group_labels = get_group_labels(companies)
    return group_labels, totals

def drop_duplicates(df:pd.DataFrame)->pd.DataFrame:
    df.drop_duplicates(inplace=True)
    # print(f"shape after removing duplicates:{df.shape}")
    df.drop(df[df['issuerTradingSymbol'] == 'issuerTradingSymbol'].index, inplace=True)
    # print(f"shape after cleaning extra header rows:{df.shape}")
    return df

def change_col_datatype(df:pd.DataFrame)->pd.DataFrame:
    df = df.astype({
        'Company': str,
        'issuerTradingSymbol': str,
        'ownerId': str,
        'ownerName': str,
        'pricePerShare': float,
        'securityTitle':str,
        'sharesTraded':int
    })
    
    df['transactionDate']=pd.to_datetime(df['transactionDate'])
    df['reportDate']=pd.to_datetime(df['reportDate'])
    
    print(df.info())
    return df