#Import the required Libraries
import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
from utils import utils
st.set_page_config(layout = 'wide')
import plotly.graph_objects as go

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path,
        names = [
            'Company', 'issuerTradingSymbol',
            'ownerId', 'ownerName',
            'pricePerShare', 'reportDate',
            'securityTitle', 'sharesTraded',
            'transactionDate'])
    df = utils.drop_duplicates(df)
    df = utils.change_col_datatype(df)
    return df

def add_total_trades_graph(filtered_df, company_codes):
    fig = go.Figure()
    group_labels, totals = utils.get_total_trades(filtered_df, company_codes)
    trace1 = go.Bar(x=group_labels, y=totals, xaxis='x2', yaxis='y2',
            marker=dict(color='#0099ff'),
            name='Total shares trades per company')
    fig.add_trace(trace1)
    st.plotly_chart(fig, use_container_width=True)

data = load_data("data/form4.csv")

header = st.container()
inputt = st.container()
output = st.container()
analysis = st.container()

with header:
    st.title("Scraping SEC for inside trading information")

with inputt:
    st.header("Input Criteria")
    # col1 = st.columns(1)
    company_codes = st.multiselect(
    'Select one or more companies',
    options = ['AAPL', 'TSLA', 'MSFT', 'GOOGL'],
    format_func=utils.formatted_company_label
    )
    
with output:
    st.header("Scraped Data")
    # st.write('You selected:', company_ciks)
    if company_codes:        
        filtered_df = data[data['issuerTradingSymbol'].isin(company_codes)]
        if filtered_df.shape[0]:
            st.subheader("Following data is stored as csv after scraping:")
            st.table(filtered_df)    
            st.subheader("Total shares acquired by insiders for different company:")
            add_total_trades_graph(filtered_df, company_codes)
        else:
            st.write("No data found for this company. Please try another one")
    
        

    

