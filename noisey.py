import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


df = pd.read_csv('Monthly_Transportation_Statistics.csv')
df[ 'Date' ] = pd.to_datetime(df['Date'])
df[ 'covid' ] = df["Date"] > '11/01/2019'
covid_df = df.loc[df['Date'] > '11/01/2019']
noncovid_df = df.loc[df['Date'] <= '11/01/2019']
st.set_page_config(page_title = "Data 102 Project Tool", layout =  "wide")
st.title("Data 102 Transportation Tool")


x_axis = st.sidebar.selectbox("Pick Your X Axis Graph", df.columns)
option = st.sidebar.selectbox("Change X Proportion in Terms of Governement Spending Total?",["Yes", 'No'])
y_axis = st.sidebar.selectbox("Pick Your Y Axis Graph", df.columns)
covid_era = st.sidebar.selectbox("Pick Your Data Ranges", ['Covid ( > 12/2019)', "Pre-Covid", "All Dates"])
width = st.sidebar.slider("plot width", 1, 15, 15)
height = st.sidebar.slider("plot height", 1, 15, 2)
if covid_era == "Covid ( > 12/2019)":
    sdata = covid_df
elif covid_era == "Pre-Covid":
    sdata = noncovid_df
else:
   sdata = df

if option == "Yes":
    new_df = sdata.copy()[['Date', x_axis, y_axis, 'covid', 'State and Local Government Construction Spending - Total']]
    st.title("IMPORTANT")
    st.write("Original Data Frame: ")
    st.dataframe(new_df)
    st.subheader("By utilizing Proportions We Dropped: " + str(abs(new_df.shape[0] - new_df.dropna().shape[0])) + " Rows")
    new_df = new_df.dropna() 
    new_df[x_axis] = (new_df[x_axis])/new_df['State and Local Government Construction Spending - Total']
else:
    new_df = sdata.copy()
    
st.subheader("OUR DATAFRAME")
st.dataframe(new_df)
st.subheader("Line Plot")
figline = plt.figure(figsize=(width, height))
sns.lineplot(x = x_axis, y = y_axis, data = new_df, color = 'r')
if option == "Yes":
    plt.xlabel(x_axis + " (In Proportion to State and Local Government Construction Spending - Total)")
else:
    plt.xlabel(x_axis)
plt.ylabel(y_axis)
st.pyplot(figline)

st.subheader("Scatter Plot")
figline = plt.figure(figsize=(width, height))
sns.scatterplot(x = x_axis, y = y_axis, data = new_df, color = 'r',  hue = "covid")
if option == "Yes":
    plt.xlabel(x_axis + " (In Proportion to State and Local Government Construction Spending - Total)")
else:
    plt.xlabel(x_axis)
plt.ylabel(y_axis)
st.pyplot(figline)

st.title("Multi-Period Plot")
figline = plt.figure(figsize=(width, height))
sns.lineplot(x = x_axis, y = y_axis, data = new_df, label = "Transition Period")
sns.lineplot(x = x_axis, y = y_axis, data = covid_df, label = "Covid Times")
sns.lineplot(x = x_axis, y = y_axis, data = noncovid_df, label = "Non-Covid Times")
if option == "Yes":
    plt.xlabel(x_axis + " (In Proportion to State and Local Government Construction Spending - Total)")
else:
    plt.xlabel(x_axis)
plt.ylabel(y_axis)
st.pyplot(figline)

st.title("Static Plots")
st.write("The Graph below is a scatter plot w/ Dates and Highway Fatalities. The size of each dot is dependent on the US's spending. Notice that there isn't much difference at all")
figline = plt.figure(figsize=(width, height))
plt.scatter(x = df["Date"], y = df["Highway Fatalities"], s = np.log(df['State and Local Government Construction Spending - Total']), alpha=0.5)
plt.xlabel("Date")
plt.ylabel("Highway Fatalities")
st.pyplot(figline)
