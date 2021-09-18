from genericpath import exists
import streamlit as st
import datetime
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import altair as alt
import os 

x = pd.read_csv( './data/sample/sample.csv',names=["forecast"] )
y = pd.read_csv( './data/sample/sampleInputData.csv')
y = pd.DataFrame(y['date'])
y['date'] = pd.to_datetime(y.date,format = '%Y-%m-%d %H:%M:%S') 
y['date'] = y['date'].dt.tz_localize('Asia/Shanghai')
x = pd.concat([x,y],axis=1)
st.title('forecast')
st.dataframe(x)
date_en = st.date_input('預測資料')
st.write('your selection',date_en)
s = date_en.strftime('%Y_%m_%d')
if os.path.exists('./data/loadfueltype/'+s+'.csv'):
    picked = pd.read_csv('./data/loadfueltype/'+s+'.csv')
    st.dataframe(picked)
    print(x)
else:
    st.write('目前沒有相關資料，請選擇其他日期')
st.subheader('sample.csv')
plot = alt.Chart(x).mark_line().encode(
    alt.X('hoursminutes(date):T', title='hour of day'),
    alt.Y('forecast:Q', title='Forecast'),
).properties(
    width=700,
    height=330
)
st.write(plot)
