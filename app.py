from genericpath import exists
import streamlit as st
import datetime
from datetime import timedelta
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import altair as alt
import os 

d = st.date_input("請選擇欲觀察電力負載曲線",datetime.date.today(),min_value=datetime.date.today(),max_value = datetime.date.today()+timedelta(days=1))
if d == datetime.date.today():    
    x = pd.read_csv( './data/sample/sample.csv',names=["預測負載"] ,index_col = False)
else:
    x = pd.read_csv( './data/sample/sample_2.csv',names=["預測負載"] ,index_col = False)
y = pd.read_csv( './data/sample/sampleInputData.csv',index_col=False)
today = pd.read_csv('https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadareas.csv',names=["time","north","central","south","east"],index_col = False)
today['當日總負載'] = today.sum(axis=1)*10
today.drop(["time","north","central","south","east"], axis=1, inplace=True)
y = pd.DataFrame(y['date'])
y['date'] = pd.to_datetime(y.date,format = '%Y-%m-%d %H:%M:%S') 
y['date'] = y['date'].dt.tz_localize('Asia/Shanghai')
x = pd.concat([x,y,today],axis=1)
if d !=  datetime.date.today():
    del x["當日總負載"]
st.title('電力負載預測')
st.subheader('預測資料')
data = x.melt('date',var_name='數據',value_name='負載量（Mw）')
plot = alt.Chart(data).mark_line().encode(
    alt.X('hoursminutes(date):T', title='時間'),
    y='負載量（Mw）:Q',
    color='數據:N',
    tooltip=['hoursminutes(date):T','負載量（Mw）']
).properties(
    width=700,
    height=330
)
st.write(plot)
x['time'] = pd.to_datetime(x['date']).dt.time
max_value =  x['預測負載'].max()
my_max_ind = x['預測負載'].idxmax()   
st.write('預測最大負載值:',max_value)
st.markdown("")
st.write("預測最大負載時間:",x.at[my_max_ind,'time'])
