import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Class 17")

st.header("Data")
st.write("This section is for showing data structure")

df = pd.read_excel('sample_-_superstore.xls')
cond = df["Country/Region"]=="United States"
df = df[cond]

# st.write(df.head(3))
all_states = df['State/Province'].unique()
target_states = st.multiselect("Choose states", options=all_states, default=["New York", "Massachusetts"])
df = df[df['State/Province'].isin(target_states)] # connecting target_states with later visualizations
                                                  #by slicing 'df' based on target_states

st.write(df.head(5))

st.header("Visualizations")

col1,col2 = st.columns([7,3])
with col1:
    #step 1: calculate sum of profits by state
    profit_sums_state = df.groupby('State/Province')['Profit'].sum()

    #step 2: sum of sales by state
    sales_sums_state = df.groupby('State/Province')['Sales'].sum()

    #step 3: calc. profit margin by dividing
    profit_margin_state = profit_sums_state / sales_sums_state
    profit_margin_state = profit_margin_state.reset_index(name='Profit Margin')

    fig1 = px.choropleth(
        locations = profit_margin_state['State/Province'],
        locationmode = 'USA-states',
        scope= 'usa',
        color = profit_margin_state['Profit Margin'],
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig1, width="stretch")

with col2:
    profit_sums_cat = df.groupby('Category')['Profit'].sum()
    sales_sums_cat = df.groupby('Category')['Sales'].sum()
    profit_margin_cat = profit_sums_cat / sales_sums_cat
    profit_margin_cat = profit_margin_cat.reset_index(name="Profit Margin Cat.")

    fig2 = px.bar(
        profit_margin_cat,
        x = 'Category',
        y = 'Profit Margin Cat.',
        color = 'Category'
    )
    st.plotly_chart(fig2, width="stretch")

col3, col4 = st.columns([7,3])
with col3:
    df['YM'] = pd.to_datetime(df['Order Date']).dt.strftime('%Y-%m')
    a = df.groupby(['Category', 'YM'])['Profit'].sum()
    b = df.groupby(['Category', 'YM'])['Sales'].sum()
    profit_margin_cat_ym = a/b
    profit_margin_cat_ym = profit_margin_cat_ym.reset_index(name="Profit Margin")
    profit_margin_cat_ym

    fig3 = px.line(
        profit_margin_cat_ym,
        x='YM',
        y= 'Profit Margin',
        color='Category'
    )
    st.plotly_chart(fig3, width="stretch")
                
