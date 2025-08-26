# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title='Superstore Sales Analysis Dashboard',
    page_icon='📈',
    layout = 'wide',
    initial_sidebar_state= 'expanded'
)

# Function to load dataset
@st.cache_data
def load_data() :
    return pd.read_csv('Dataset/superstore.csv')

# Load Dataset
df = load_data()

# Convert datatype from object to datetime
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

# ---------SIDEBAR ---------
# Sidebar for filter and navigation
st.sidebar.header('⚙️ Dashboard Filter')

# Make a new column "year"
df['year'] = df['order_date'].dt.year

# Make a list of unique year
year_list = df['year'].unique().tolist() # take all unique years

# Sort year
year_list.sort(reverse=True)

# Add "All" as part of filter
year_list = ['All'] + year_list 

# Year filter
st.sidebar.subheader('📅 Year Filter')
selected_year = st.sidebar.selectbox('Select Year', options=year_list, index = 0 ) # set default to "All Year"

# Apply year filter
if selected_year == 'All' :
    df_filtered = df.copy()
else :
    df_filtered = df[df['year'] == selected_year]

# Make a list of customer segment
segment_list = df['segment'].unique().tolist()

# Customer segment filter
st.sidebar.subheader('👥 Segment Filter')
selected_segment = st.sidebar.multiselect('Select Segment', options=segment_list, default=segment_list)

# Apply segment filter
df_filtered = df_filtered[df_filtered['segment'].isin(selected_segment)]

# Make a list of region 
region_list = df['region'].unique().tolist()

# Region filter
st.sidebar.subheader('📍 Region Filter')
selected_region = st.sidebar.multiselect('Select Region', options=region_list, default=region_list) 

# Apply region filter
df_filtered = df_filtered[df_filtered['region'].isin(selected_region)]

# ----- MAIN PAGE ----
# Title
st.title('🛒 SUPERSTORE DASHBOARD')
st.markdown("Superstore is a fictional retail company in the United States. This project aims to gain comprehensive insights into Superstore's sales performance, customer behaviour, and product analysis over the period of 2014 - 2017. Insights from in-depth analysis will deliver data-driven recommendations to boost its revenue")

# Border line
st.markdown('---')

# Create tabs 
tab_sales, tab_products, tab_customer = st.tabs(['Sales Analysis', 'Product Analysis', 'Customer Analysis'])

# ---Page 1 : Sales Analysis ---
with tab_sales :
    st.header('Sales Performance Analysis')

    # KPI metrics
    st.subheader('KPI Metrics')

    # create columns
    col1, col2, col3, col4 = st.columns([3,3,3,3])

    # Calculate metrics
    total_profit = df_filtered['profit'].sum()
    total_order = df_filtered['order_id'].nunique()
    quantity_sold = df_filtered['quantity'].sum()
    total_sales = df_filtered['sales'].sum()

    # make metrics
    with col1 :
        st.metric(label = 'Total Sales', value = f'${total_sales/1000000:.2f}M')
    with col2 :
        st.metric(label='Total Profit', value = f'${total_profit/1000:.2f}K')
    with col3 :
        st.metric(label='Total Transactions', value = total_order)
    with col4 :
        st.metric(label='Total Quantity Sold', value = f'{total_profit/1000:.2f}K')

    st.markdown("---")

    # monthly sales
    st.subheader('Monthly Sales Trend')
    # make a new column "month_name" and "month_num"
    df_filtered['month_name'] = df_filtered['order_date'].dt.strftime('%B')
    df_filtered['month_num'] = df_filtered['order_date'].dt.month

    # data aggregation
    df_monthly = df_filtered.groupby('month_name').agg(
        total_sales= ('sales', 'sum'),
        total_profit=('profit', 'sum'),
        month_num=('month_num', 'unique') #include month_num for sorting
    ).reset_index()

    df_monthly = df_monthly.sort_values('month_num')

    # code below is referenced from geeks for geeks
    # create subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # main y-axis
    fig.add_trace(
        go.Scatter(x=df_monthly['month_name'], y=df_monthly['total_sales'], name='Sales'), secondary_y=False)
    
    # secondary y-axis
    fig.add_trace(
        go.Scatter(x=df_monthly['month_name'], y=df_monthly['total_profit'], name='Profit'), secondary_y=True)
    
    # add title
    fig.update_layout(title_text = 'Sales and Profit by Month')

    # add x-axis name
    fig.update_xaxes(title_text='Month')

    # add y-axes names
    fig.update_yaxes(title_text='Sales ($)', secondary_y=False)
    fig.update_yaxes(title_text='Profit ($)', secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ----geographic analysis-----
    # create two columns
    st.subheader('Sales by Geography')
    col5, col6 = st.columns([5,3])

    with col5 :
        # sales by state
        # data aggregation by state
        df_state = df_filtered.groupby('state')['sales'].sum().reset_index()

        # add column "state_code"
        # code below is referenced from 
        # https://medium.com/geekculture/create-a-choropleth-map-of-state-unemployment-rates-with-plotly-1354050e0cfd
        code_dict = {'Alabama': 'AL',
            'Alaska': 'AK',
            'Arizona': 'AZ',
            'Arkansas': 'AR',
            'California': 'CA',
            'Colorado': 'CO',
            'Connecticut': 'CT',
            'Delaware': 'DE',
            'District of Columbia': 'DC',
            'Florida': 'FL',
            'Georgia': 'GA',
            'Hawaii': 'HI',
            'Idaho': 'ID',
            'Illinois': 'IL',
            'Indiana': 'IN',
            'Iowa': 'IA',
            'Kansas': 'KS',
            'Kentucky': 'KY',
            'Louisiana': 'LA',
            'Maine': 'ME',
            'Maryland': 'MD',
            'Massachusetts': 'MA',
            'Michigan': 'MI',
            'Minnesota': 'MN',
            'Mississippi': 'MS',
            'Missouri': 'MO',
            'Montana': 'MT',
            'Nebraska': 'NE',
            'Nevada': 'NV',
            'New Hampshire': 'NH',
            'New Jersey': 'NJ',
            'New Mexico': 'NM',
            'New York': 'NY',
            'North Carolina': 'NC',
            'North Dakota': 'ND',
            'Ohio': 'OH',
            'Oklahoma': 'OK',
            'Oregon': 'OR',
            'Pennsylvania': 'PA',
            'Rhode Island': 'RI',
            'South Carolina': 'SC',
            'South Dakota': 'SD',
            'Tennessee': 'TN',
            'Texas': 'TX',
            'Utah': 'UT',
            'Vermont': 'VT',
            'Virginia': 'VA',
            'Washington': 'WA',
            'West Virginia': 'WV',
            'Wisconsin': 'WI',
            'Wyoming': 'WY'}

        df_state['state_code'] = df_state['state'].map(code_dict)
        df_state['Total Sales'] = df_state['sales'].apply(lambda x: f'${x/1000:.2f}K') # code from chatGPT

        # create a choropleth map
        fig_map = px.choropleth(df_state,
                                locations = 'state_code',
                                color='sales',
                                locationmode='USA-states',
                                title = 'Sales by State',
                                scope = 'usa',
                                hover_data={'state' : True, 'sales' : False, 
                                            'state_code' : False, 'Total Sales' : True})
        st.plotly_chart(fig_map, use_container_width=True)

    

    # top 10 cities
    with col6 :
        # data aggregation
        top_10_cities = df_filtered.groupby('city')['sales'].sum().reset_index().sort_values('sales', ascending=False).head(10)
        bar_city = px.bar(top_10_cities, x='sales', y='city', orientation='h', title='Top 10 Cities by Sales')
        bar_city.update_xaxes(title_text='Total Sales ($)')
        bar_city.update_yaxes(title_text='City')
        st.plotly_chart(bar_city, use_container_width=True)

    st.markdown("---")

    # ----product&shipping
    st.subheader('Total Order by Product Category and Shipping')
    # create 2 columns
    col7, col8 = st.columns(2)
    
    # sales by product category
    with col7 :
        # data aggregation
        df_category = df_filtered.groupby('category').agg(
            total_order = ('order_id', 'nunique'),
            total_sales = ('sales', 'sum')).reset_index()
        df_category.columns = ['Category', 'Total Order', 'Total Sales']
        # visualization
        pie_category = px.pie(df_category, values='Total Order', names='Category')
        st.plotly_chart(pie_category, use_container_width=True)
    
    # sales by shipping
    with col8 :
        # data aggregation
        df_shipping = df_filtered.groupby('ship_mode')['order_id'].nunique().reset_index()
        df_shipping.columns = ['Shipping Mode', 'Total Order']
       
        # visualization
        pie_shipping = px.pie(df_shipping, values='Total Order', names='Shipping Mode')
        st.plotly_chart(pie_shipping, use_container_width=True)
    
    st.markdown('---')

# ---Page 2 : Product Analysis ---
with tab_products :
    st.header('Product Analysis')
    st.subheader('Sales by Product Category and Subcategory')
    # Sales by category and sub-category
    col_category, col_sub = st.columns(2)
    
    # sales by category
    with col_category :
        bar_category = px.bar(df_category, x = 'Category', y='Total Sales', title = 'Sales by Category')
        bar_category.update_yaxes(title_text='Total Sales ($)')
        bar_category.update_xaxes(title_text='Category')
        st.plotly_chart(bar_category, use_container_width=True)
    
    # sales by sub-category
    with col_sub :
        # data aggregation
        df_sub = df_filtered.groupby('subcategory')['sales'].sum().reset_index()
        df_sub.columns = ['Sub-category', 'Total Sales']
        bar_subcategory = px.bar(df_sub, x = 'Sub-category', y='Total Sales', title = 'Sales by Sub-category')
        bar_subcategory.update_yaxes(title_text='Total Sales ($)')
        bar_subcategory.update_xaxes(title_text='Sub-category')
        st.plotly_chart(bar_subcategory, use_container_width=True)
    
    st.markdown('---')

    st.subheader('Top 10 Most Sold Products')


    # Data aggregation
    df_products = df_filtered.groupby('product_name').agg(
        quantity_sold = ('quantity', 'sum'),
        total_sales = ('sales', 'sum'),
        total_profit = ('profit', 'sum'),
        avg_discount = ('discount', 'mean'),
        category = ('category', 'first')
    ).reset_index()

    # round values
    df_products = df_products.round({
        'total_sales' :2,
        'total_profit' :2,
        'avg_discount' :2}
    )

    # Top 10 most sold products  
    top_10_sold = df_products.sort_values('quantity_sold', ascending=False).head(10)
    
        
    table_most_sold = go.Figure(data=[go.Table(
        header=dict(values=['Product', 'Total Quantity', 'Total Sales ($)', 'Total Profit ($)', 'Avg Discount'],fill_color = 'lightskyblue'), 
        cells=dict(values=[top_10_sold['product_name'], top_10_sold['quantity_sold'],
                        top_10_sold['total_sales'], top_10_sold['total_profit'],
                        top_10_sold['avg_discount']], fill_color = 'lightcyan'))])

    st.plotly_chart(table_most_sold, use_container_width=True)
    st.markdown('---')

    # Top 10 most profitable products
    st.subheader('Top 10 Most Profitable Products')
    top_10_profitable = df_products.sort_values('total_profit', ascending=False).head(10)
    table_most_profitable = go.Figure(data=[go.Table(
        header=dict(values=['Product', 'Total Profit ($)', 'Total Quantity', 'Total Sales ($)', 'Avg Discount'],fill_color = 'lightskyblue'), 
        cells=dict(values=[top_10_profitable['product_name'], top_10_profitable['total_profit'],
                            top_10_profitable['quantity_sold'],top_10_profitable['total_sales'],
                            top_10_profitable['avg_discount']], fill_color = 'lightcyan'))])

    st.plotly_chart(table_most_profitable, use_container_width=True)
    st.markdown('---')

    # Total Sales vs Total Profit 
    st.subheader('Total Sales vs Total Profit')
    df_products.columns = ['Product', 'Total Quantity', 'Total Sales', 'Total Profit',
                           'Avg Discount', 'Category']
    scatter_products = px.scatter(df_products, x='Total Sales', y='Total Profit', color = 'Category')
    st.plotly_chart(scatter_products, use_container_width=True)
    st.markdown('---')

# ---Page 3 : Customer Analysis ---
with tab_customer:
    st.header('Customer Analysis')
    # RFM Analysis
    # Make a new dataframe with customer id, customer name, and last transaction date
    df_recency = pd.DataFrame(df_filtered.groupby(['customer_id', 'customer_name'])['order_date'].max().sort_values(ascending=False).reset_index())
    df_recency.rename(columns = {'order_date':'last_transaction'}, inplace=True)

    # calculate days since last transaction
    current_date = df_filtered['order_date'].max() + timedelta(days=1)
    df_recency['recency'] = (current_date - df_recency['last_transaction']).dt.days
    df_recency.dropna(subset=['recency'])

    # Assign R score based on percentile
    df_recency['r_score'] = pd.qcut(df_recency['recency'], 5, labels = [5,4,3,2,1])

    # Make a new dataframe with customer id, customer name, and frequency
    df_frequency = pd.DataFrame(df_filtered.groupby(['customer_id', 'customer_name'])['order_id'].nunique().sort_values(ascending=False).reset_index())
    df_frequency.rename(columns = {'order_id':'frequency'}, inplace=True)
    df_frequency.dropna(subset=['frequency'])

    # Assign F score based on percentile
    df_frequency['f_score'] = pd.qcut(df_frequency['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
        

    # Make a new dataframe with customer id, customer name, and monetary
    df_monetary = pd.DataFrame(df_filtered.groupby(['customer_id', 'customer_name'])['sales'].sum().sort_values(ascending=False).reset_index())
    df_monetary.dropna(subset=['sales'])
    
    # Assign M score based on percentile
    df_monetary['m_score'] = pd.qcut(df_monetary['sales'], 5, labels = [1,2,3,4,5])
    
    # merge all dataframes
    df_merged = pd.merge(df_recency, df_frequency, on = ['customer_id', 'customer_name'], how = 'inner')
    df_merged = pd.merge(df_merged, df_monetary, on = ['customer_id', 'customer_name'], how = 'inner')

    # calculate rfm score
    df_merged['rfm'] = (df_merged['r_score'].astype(str) +
                        df_merged['f_score'].astype(str) +
                        df_merged['m_score'].astype(str))
    df_merged['rfm']= df_merged['rfm'].astype(int)

    # customer segmentation based on rfm score
    def customer_segmentation(rfm):
        if 511 <= rfm <= 555:
            return 'Champions'
        elif 451 <= rfm <= 510:
            return 'Loyal'
        elif 351 <= rfm <= 450:
            return 'Potential'
        elif 151 <= rfm <= 350:
            return 'At Risk'
        else:
            return 'Uncategorized'

    df_merged['customer_segment'] = df_merged['rfm'].apply(customer_segmentation)


    st.subheader('Proportion of Customer Segmentation (RFM Analysis)')
    pie_segment = px.pie(df_merged,  names='customer_segment')
    st.plotly_chart(pie_segment, use_container_width=True)
    st.markdown('---')

    # total profit by each customer segment
    st.subheader('Total Profit and Average Discount by Customer Segmentation')
    col_profit_customer, col_disc_customer = st.columns(2)


    #Data aggregation profit
    df_profit_disc = df_filtered.groupby('customer_id').agg(
        total_profit = ('profit', 'sum'),
        avg_discount=('discount', 'mean')
    )

    df_profit_disc.rename(columns={'total_profit' : 'Total Profit',
                                   'avg_discount' : 'Avg Discount' }, inplace=True)
    # merge with RFM dataframe
    df_merged = pd.merge(df_merged, df_profit_disc, on = 'customer_id', how='left' )
    
    with col_profit_customer:
        df_profit_rfm = df_merged.groupby('customer_segment')['Total Profit'].sum().reset_index()
        bar_profit_rfm = px.bar(df_profit_rfm, x='Total Profit', y = 'customer_segment', orientation='h', title = 'Total Profit by Customer Segmentation')
        st.plotly_chart(bar_profit_rfm, use_container_width=True)
    
    with col_disc_customer :
        df_discount_rfm = df_merged.groupby('customer_segment')['Avg Discount'].mean().reset_index()
        bar_discount_rfm = px.bar(df_discount_rfm, x='Avg Discount', y = 'customer_segment', orientation='h', title = 'Avg Discount by Customer Segmentation')
        st.plotly_chart(bar_discount_rfm, use_container_width=True)

    st.markdown('---')
    # Top 10 customers who generated the most profit
    st.subheader('Top 10 Customers Generating the Most Profit')
    top_10_customers = df_merged.sort_values('Total Profit', ascending=False).head(10)
    # round values
    top_10_customers = top_10_customers.round(
        {'Total Profit' : 2,
         'sales' : 2}
    )
    table_most_profitable_customer = go.Figure(data=[go.Table(
        header=dict(values=['Customer Name', 'Customer Segment', 'Total Profit ($)',  'Total Sales ($)'],fill_color = 'lightskyblue'), 
        cells=dict(values=[top_10_customers['customer_name'], top_10_customers['customer_segment'],
                           top_10_customers['Total Profit'],top_10_customers['sales']],
                            fill_color = 'lightcyan'))])

    st.plotly_chart(table_most_profitable_customer, use_container_width=True)
    st.markdown('---')
