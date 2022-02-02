#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 15:50:12 2022

@author: mho
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pickle 

st.title("Insurance Premium")

url = r"https://raw.githubusercontent.com/mhcode001/GA_HW3_App/main/insurance_premiums.csv"

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
    
    x_axis = st.sidebar.selectbox("Choose column for X-axis",['age','sex','children', 'smoker', 'region'])
    
    y_axis = st.sidebar.selectbox("Choose column for y-axis",['charges'])
   
    chart_type = st.sidebar.selectbox("Choose Your Chart Type",['line','bar','area'])
     
    
    if chart_type == 'line':
        grouping = create_grouping(x_axis, y_axis)
        st.line_chart(grouping)
        
    elif chart_type == 'bar':
        grouping = create_grouping(x_axis, y_axis)
        st.bar_chart(grouping)
                
    elif chart_type == 'area':
        fig = px.strip(df[[x_axis, y_axis]], x=x_axis, y=y_axis)
        st.plotly_chart(fig)    
        
    st.write(df)
    
else:
    st.text("Choose Options to the Side to Explore the Model")

    model = load_model()

    sex = st.sidebar.radio('Choose Sex', ['female', 'male'])

    smoker = st.sidebar.radio('Smoker', ['yes', 'no'])

    age = st.sidebar.slider("Age")

    bmi = st.sidebar.slider("Select BMI", 0.0, 100.0)
    
    children = st.sidebar.number_input('Number of Children',0)
    
    region = st.sidebar.selectbox("Region", df['region'].unique().tolist())    
    
    sample = {
    'sex': sex,
    'smoker': smoker,
    'age': age,
    'region': region,
    'bmi':bmi,
    'children': children
    }

    sample = pd.DataFrame(sample, index = [0])
    prediction = model.predict(sample)[0]
    
    st.title(f"Predicted Insurance Premium: ${int(prediction)}")
    

