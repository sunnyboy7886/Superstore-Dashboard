import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly_express as px
import matplotlib as mp
from streamlit_option_menu import option_menu
import warnings
warnings.filterwarnings(action='ignore')

st.set_page_config(
    page_title="Superstore-Dashboard",
    page_icon=":bar-chart:",
    layout="wide",
    initial_sidebar_state="auto"
)

st_hide_style = '''
<style>
#MainMenu {visibility: hidden}
Header {visibility: hidden}
Footer { visibility: hidden}
div.block-container {padding : 1rem}
</style>
'''
st.markdown(st_hide_style, unsafe_allow_html=True)

st.title("Super Store Dashboard :chart:")

st.cache_data()
def read_file():
    df = pd.read_csv('SampleSuperstore.csv')
    return df
  
df = read_file()  

left, middle, right = st.columns(3)
with left:
    region = st.multiselect('Select Region', options=df['Region'].unique())
    if not region:
        df1 = df.copy()
    else:
        df1= df[df["Region"].isin(region)]                              
with middle:
    state = st.multiselect('Select State', options=df1['State'].unique())
    if not state:
        df2 = df1.copy()
    else:
        df2 = df1[df1['State'].isin(state)]
with right:
    city = st.multiselect('Select City', options=df2['City'].unique())
    if not city:
        df3 = df2.copy()
    else:
        df3 = df2[df2['City'].isin(city)]

if not region and not state and not city:
    filterdf =  df.copy()
elif not state and not city:
    filterdf = df[df["Region"].isin(region)]
elif not region and not city:
    filterdf = df[df['State'].isin(state)]
elif not region and not state:
    filterdf = df[df['City'].isin(city)]
elif not city:
    filterdf = df[df["Region"].isin(region) & df['State'].isin(state)]
elif not state:
    filterdf = df[df["Region"].isin(region) & df['City'].isin(city)]
elif not region:
    filterdf = df[df['State'].isin(state) & df1['City'].isin(city)]
elif region and state and city:
    filterdf = df[df['Region'].isin(region) & df['State'].isin(state) & df['City'].isin(city)]

st.divider()

# st.dataframe(filterdf, height=200)
   
Total_sales =  round(filterdf['Sales'].sum(),2)

Total_quantity = round(filterdf['Quantity'].sum(),2)

Total_profit = round(filterdf['Profit'].sum(),2)

left_col,middle_col,right_col = st.columns(3)
with left_col:
    st.metric('Total Sales', f"{Total_sales} $")
with middle_col:
    st.metric('Total Quantity Sold', f"{Total_quantity} units")
with right_col:
    st.metric('Total Profit Earned', f"{Total_profit} $")
    
regionwise_sales_profit = filterdf.groupby(by=['Region'], as_index=False).agg({'Profit' : sum, 'Sales' : sum})

regionwise_profit_graph = px.bar(data_frame=regionwise_sales_profit, x= regionwise_sales_profit['Region'], y= ['Sales','Profit'], text_auto=',.2f' , barmode='group', title= 'Region wise Sales and Profit')
st.plotly_chart(regionwise_profit_graph,use_container_width= True)

with st.expander('Download Regionwise, State and City Sales and Profit'):
    regionwise_sales_profit_csv = filterdf.groupby(by=['Region', 'State', 'City'], as_index=False).agg({'Sales': sum, 'Profit': sum})
    st.write(regionwise_sales_profit_csv.style.background_gradient(cmap='Oranges'))
    csv = regionwise_sales_profit_csv.to_csv(index=False, encoding='utf-8')
    st.download_button('Download sales and profit', data=csv, file_name='region,state and citywise sales and profit.csv', mime='text/csv')

categorywise_profit = filterdf.groupby(by='Category', as_index=False)['Profit'].sum()

categorywise_profit_graph = px.pie(data_frame=categorywise_profit, names= 'Category', values='Profit', hole= 0.5, title= 'Category Wise Profit')

categorywise_profit_graph.update_traces(text= categorywise_profit['Category'])

categorywise_sales = filterdf.groupby(by='Category', as_index=False)['Sales'].sum()

categorywise_sales_graph = px.pie(data_frame=categorywise_sales, names= 'Category', values='Sales', hole= 0.5, title= 'Category Wise Sales')

categorywise_sales_graph.update_traces(text= categorywise_profit['Category'])

left_col, right_col = st.columns(2)
with left_col:
    st.plotly_chart(categorywise_profit_graph, use_container_width=True)
with right_col:
    st.plotly_chart(categorywise_sales_graph, use_container_width=True)
    
segmentwise_sales_profit = filterdf.groupby('Segment', as_index=False).agg(
    {
        'Sales': sum,
        'Profit' : sum
    })

segmentwise_sales_profit_graph = px.bar(segmentwise_sales_profit, x= segmentwise_sales_profit['Segment'], y= [segmentwise_sales_profit['Sales'], segmentwise_sales_profit['Profit']], text_auto=',.2f', title= 'Segment Wise Sales and Profit', barmode='group')

st.plotly_chart(segmentwise_sales_profit_graph, use_container_width=True)

subcategory_sales_profit = filterdf.groupby(by=['Sub-Category'], as_index=False).agg({'Sales': sum, 'Profit': sum})

subcategory_sales_profit_graph = px.bar(data_frame=subcategory_sales_profit, x='Sub-Category', y=['Sales','Profit'], text_auto=',.2s', title='Sub-Category wise Sales and Profit', barmode='group', height=600)
st.plotly_chart(subcategory_sales_profit_graph, use_container_width=True)