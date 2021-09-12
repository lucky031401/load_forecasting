# -*- coding: utf-8 -*-
"""predCode.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ORrixCN37nQATteCAAr8CFoggNSGZEcu
"""

import pandas as pd
import numpy as np

# 設定輸入資料、輸出資料的長度
input_length = 144
output_length = 144

x = pd.read_csv( '../data/sampleInputData.csv', index_col=0 )
x_load = np.array(x.loc[ :, 'load' ])
x_bodyComfort = np.array(x.loc[ :, 'bodyComfort' ])
x_lastWeek = np.array(x.loc[ :, 'lastWeek' ])


x_load = np.reshape( x_load, (len(x_load), 1) )
x_bodyComfort = np.reshape( x_bodyComfort, (len(x_bodyComfort), 1) )
x_lastWeek = np.reshape( x_lastWeek, (len(x_lastWeek), 1) )

# normalization
from sklearn.preprocessing import MinMaxScaler
# 需要兩個轉換模型 因為單位不同
scaler_load = MinMaxScaler(feature_range=(0,1))
scaler_bodyComfort = MinMaxScaler(feature_range=(0,1))
x_load = scaler_load.fit_transform(x_load)
x_lastWeek = scaler_load.transform(x_lastWeek)
x_bodyComfort = scaler_bodyComfort.fit_transform(x_bodyComfort)

x_input = np.concatenate( (x_load,x_bodyComfort), axis=1 )
x_input = np.concatenate( (x_input,x_lastWeek), axis=1 )

x_input = np.reshape(x_input,(1,x_input.shape[0],x_input.shape[1]))

print( x_input.shape )

from keras.models import Sequential
from keras.layers import Dense,Activation,CuDNNLSTM,LSTM
from keras import optimizers

model = Sequential()
model.add(LSTM(288,return_sequences=True,input_shape=(x_input.shape[1],x_input.shape[2]))) # 此處輸入特徵(feature)為3喔!
model.add(LSTM(144,return_sequences=False))
model.add(Dense(144,activation='relu'))
model.add(Dense(output_length))

# 輸出模型摘要資訊
model.summary()
# load model param
model.load_weights('../data/19-0.0013-0.0015.hdf5')



# 以模型預估
predResult = model.predict( x_input )

# 轉回原數值(actual value)
predResult = scaler_load.inverse_transform(predResult)

# to one dim
predResult = np.reshape( predResult,(predResult.shape[1]) )

pd.DataFrame(predResult).to_csv("../data/sample.csv",header=None,index=None)

print("forkin"+"me")



