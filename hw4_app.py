#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 15:50:12 2022

@author: mho
"""

import streamlit as st
import pandas as pd
#import plotly.express as px
import pickle 

st.title("Craft Beer ABU")

url = r"https://raw.githubusercontent.com/mhcode001/GA_HW4_App/main/allcraftbeer.csv"

num_rows = st.sidebar.number_input('Select Number of Rows to Load', 
                                  min_value = 500, 
                                  max_value = 1500, 
                                  step = 100)

section = st.sidebar.radio('Choose Application Section', ['Data Explorer', 
                                                          'Model Explorer'])
print(section)

@st.cache
def load_data(num_rows):
    df = pd.read_csv(url, nrows = num_rows)
    return df

@st.cache
def create_grouping(x_axis, y_axis):
    grouping =  df.groupby(x_axis)[y_axis].mean()
    return grouping

def load_model():
    with open('pipe.pkl', 'rb') as pickled_mod:
        model = pickle.load(pickled_mod)
    return model

df = load_data(num_rows)

if section == 'Data Explorer':
    
    x_axis = st.sidebar.selectbox("Choose column for X-axis",['ibu','beer_name','style','brewery_name', 'city', 'state',  'ounces'])
    
    y_axis = st.sidebar.selectbox("Choose column for y-axis",['abv'])
   
    chart_type = st.sidebar.selectbox("Choose Your Chart Type",['line','bar'])
     
    
    if chart_type == 'line':
        grouping = create_grouping(x_axis, y_axis)
        st.line_chart(grouping)
        
    elif chart_type == 'bar':
        grouping = create_grouping(x_axis, y_axis)
        st.bar_chart(grouping)
                
  #  elif chart_type == 'area':
  #      fig = px.strip(df[[x_axis, y_axis]], x=x_axis, y=y_axis)
  #      st.plotly_chart(fig)    
        
    st.write(df)
    
else:
    st.text("Choose Options to the Side to Explore the Model")

    model = load_model()

    beer_name = st.sidebar.selectbox("Beer", sorted(df['beer_name'].unique().tolist()))

    style = st.sidebar.selectbox("Style", sorted(df['style'].unique().tolist()))
   
    brewery_name = st.sidebar.selectbox("Brewery Name", sorted(df['brewery_name'].unique().tolist()))
    
    city = st.sidebar.selectbox("City", sorted(df['city'].unique().tolist()))
    
    state = st.sidebar.selectbox("State", sorted(df['state'].unique().tolist()))
    
    ibu = st.sidebar.slider("ibu", 0.0, 150.0)

    ounces = st.sidebar.radio("ounces", ['8.4', '12', '16','24'])  

        
    sample = {
        'beer_name': beer_name,
        'style': style,
        'brewery_name': brewery_name,
        'city': city,
        'state': state,
        'ibu': ibu,
        'ounces': ounces
        }


    sample = pd.DataFrame(sample, index = [0])
    prediction = model.predict(sample)[0]
    
    st.title(f"Predicted ABV: {int(prediction)}")