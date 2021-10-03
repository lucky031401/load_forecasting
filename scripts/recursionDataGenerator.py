import os
import shutil
import json
import datetime
import pandas as pd
from copy import deepcopy

from dateutil.relativedelta import relativedelta

class BodyComfortGenerator:

    def __init__(self,pathOfDataFolder,dateOfToday):
        self.pathOfDataFolder = pathOfDataFolder

        # 理論上 只需要明天之資料，暫時使用
        self.dateOfToday = dateOfToday
        dateForPred = self.dateOfToday + datetime.timedelta(days=2) # the day of tomorrow of dateOfToday
        self.dateForPred = str(dateForPred) 

        # 暫存最終體感資料
        self.finalBodyComfort = None

        # if exist old 'tempFile', delete it (not using)
        if os.path.exists( pathOfDataFolder + '/bodyComfortData_temp' ) :
            shutil.rmtree( pathOfDataFolder + '/bodyComfortData_temp' )

        # check whether there exist a folder for put newest temporary bodycomfortData 
        if not os.path.exists( pathOfDataFolder + '/bodyComfortData_temp/' ):
            os.makedirs( pathOfDataFolder + '/bodyComfortData_temp' )

        if not os.path.exists( pathOfDataFolder + '/bodyComfortData_temp/' + self.dateForPred ):
            os.makedirs( pathOfDataFolder + '/bodyComfortData_temp/' + self.dateForPred )
    
    def getUsefulData(self):

        # 由氣象局所抓取之預報json檔案，內部包含許多資料
        # 此處只抓取其中之 體感資料，存放於 'bodyComfortData_temp'資料夾內

        number = ["001", "005", "009", "013", "017", "021", "025", "029", "033", "037",
                "041", "045", "049", "053", "057", "061", "065", "069", "073", "077", "081", "085"]

        todayDateFormateOfFile = datetime.date.strftime(self.dateOfToday, '%Y_%m_%d') # 大寫為完整，小寫為簡寫

        for j in range(len(number)):

            # 此處抓取早上六點的明日預報，抓取哪筆差異不大
            f = open( self.pathOfDataFolder+'/weather/F-D0047-' + number[j] + '/F-D0047-' + number[j] + '-'+todayDateFormateOfFile+'_06.json', mode="r",
                    encoding='utf8')  # 加encoding才可以辨識中文
            dataarr = []

            data = json.load(f)
            data = str(data)

            d = data.split(',')

            for i in range(len(d)):         # len(d) = 11290
                d[i] = d[i].replace('{', '').replace(
                    '}', '').replace(']', '').replace('[', '')


            # newdata[0]是縣市名稱、[1]是日期、之後就是資料
            newdata1 = [d[33][19:-1], d[249][14:24], d[249][14:-1], d[250][27:-1], d[252][14:-1], d[253][27:-1],
                        d[255][14:-1], d[256][27:-1], d[258][14:-1], d[259][27:-1], d[261][14:-1], d[262][27:-1], d[264][14:-1], d[265][27:-1], d[267][14:-1], d[268][27:-1], d[270][14:-1], d[271][27:-1]]
            newdata2 = []

            for i in range(len(newdata1)):
                # print("newdata1[", i, "]: ", newdata1[i])
                newdata2.append(newdata1[i])

            df1 = []
            df1 = [newdata2[1]+' 00:00', newdata2[1]+' 01:00', newdata2[1]+' 02:00', newdata2[1]+' 03:00', newdata2[1]+' 04:00', newdata2[1]+' 05:00', newdata2[1]+' 06:00', newdata2[1]+' 07:00', newdata2[1]+' 08:00', newdata2[1]+' 09:00',
                   newdata2[1]+' 10:00', newdata2[1]+' 11:00', newdata2[1]+' 12:00', newdata2[1]+' 13:00', newdata2[1]+' 14:00', newdata2[1]+' 15:00', newdata2[1]+' 16:00', newdata2[1]+' 17:00', newdata2[1]+' 18:00', newdata2[1]+' 19:00', newdata2[1]+' 20:00', newdata2[1]+' 21:00', newdata2[1]+' 22:00', newdata2[1]+' 23:00']

            Ta = [newdata1[3], newdata1[3], newdata1[3], newdata1[5], newdata1[5], newdata1[5], newdata1[7], newdata1[7], newdata1[7], newdata1[9], newdata1[9], newdata1[9],
                newdata1[11], newdata1[11], newdata1[11], newdata1[13], newdata1[13], newdata1[13], newdata1[15], newdata1[15], newdata1[15], newdata1[17], newdata1[17], newdata1[17]]

            Time = pd.Series(df1)
            Ta = pd.Series(Ta)
            redata = pd.DataFrame({'Time': Time, 'Ta': Ta})
            Result = self.pathOfDataFolder + "/bodyComfortData_temp/" + newdata1[1] + "/" + newdata1[0] + newdata1[1] + ".csv"
            redata.to_csv(Result, index=False)
            print('成功產出'+Result)

            f.close()


    def multiplyCityPercentage(self):

        # 此處將用電比例乘上各縣市體感，並且複寫 'bodyComfortData_temp' 內部資料

        # 台電所需格式為 2020年08月，進行格式轉換
        dateFormateChinese = datetime.date.strftime(self.dateOfToday, '%Y年%m月') # 大寫為完整，小寫為簡寫

        # 讀檔，各月份用電資訊
        cityPercentageFile = pd.read_csv( self.pathOfDataFolder + '/cityUsingElecPercentage.csv' )
        cityPercentageFile = pd.DataFrame(cityPercentageFile)

        if str(dateFormateChinese) in cityPercentageFile.values:
            # 此月份存在於統計資料內
            print('此月份有統計資料'+dateFormateChinese)
            matchData = cityPercentageFile.loc[cityPercentageFile['日期'] == dateFormateChinese]
            usePowerPercentage = list(matchData['縣市用電佔比(%)'])[:-1]
            
        else:
            # 若所預估之日期，資料不在統計比例內（應該都是）
            # 採用去年同月份之資料
            print('此月份無統計資料，採用去年度同月份資料')
            lastYear = self.dateOfToday - relativedelta(years=1)
            dateFormateChinese = datetime.date.strftime(lastYear, '%Y年%m月') # 大寫為完整，小寫為簡寫
            
            if str(dateFormateChinese) in cityPercentageFile.values:
                print('查找到去年之同月份資料'+dateFormateChinese)
                matchData = cityPercentageFile.loc[cityPercentageFile['日期'] == dateFormateChinese]
                usePowerPercentage = list(matchData['縣市用電佔比(%)'])[:-1]
            else:
                print('錯誤：用電比例資料從缺')


        eachCityFile = os.listdir( self.pathOfDataFolder + '/bodyComfortData_temp/' + self.dateForPred )

        for numberOfFile, file in enumerate(eachCityFile) :
            df3 = pd.read_csv( self.pathOfDataFolder + '/bodyComfortData_temp/' + self.dateForPred +'/' + file )
            df3['Ta'] = df3['Ta'].astype(float) * usePowerPercentage[numberOfFile]
            df3['Date'] = df3['Time']
            df3 = df3[['Date', 'Ta']]
            df3.to_csv( self.pathOfDataFolder + '/bodyComfortData_temp/' + self.dateForPred +'/' + file )
    
    def sumUp(self):
        
        eachCityFile = os.listdir( self.pathOfDataFolder + '/bodyComfortData_temp/' + self.dateForPred )

        # 將所有各縣市資料合併為全台灣資料
        for numberOfFile, file in enumerate(eachCityFile) :
            data = pd.read_csv( self.pathOfDataFolder + '/bodyComfortData_temp/' + self.dateForPred +'/' + file )
            if numberOfFile == 0 :
                # 第一份複製格式
                output = data[['Date', 'Ta']].copy()
            else :
                # 其餘的直接加上
                output['Ta'] = output['Ta'] + data['Ta']

        # 暫存體感資料資訊
        self.finalBodyComfort = output

    def autoRun(self):

        # 自動執行至產生整合檔案結束
        self.getUsefulData()
        self.multiplyCityPercentage()
        self.sumUp()


class LoadGenerator:
    def __init__(self,pathOfDataFolder, dateOfToday):
        self.pathOfDataFolder = pathOfDataFolder
        self.finalLoad = None
        self.lastWeekLoad = None
        self.dateOfToday = dateOfToday + datetime.timedelta(days=1)

    def readInPredResult(self):

        predResult = pd.read_csv( self.pathOfDataFolder + '/sample/sample.csv', names = ['load'])

        # 暫時存放檔案
        self.finalLoad = predResult

    
    def createLastWeekLoad(self):
        lastWeek = self.dateOfToday - relativedelta(days=7)
        print('上週負載資料為 ' + str(lastWeek) + ' 之資料')
        dateFileType = datetime.date.strftime(lastWeek , '%Y_%m_%d') # 大寫為完整，小寫為簡寫

        fileName = str(dateFileType) + '.csv'
        col_name = [ 'date', 'area1', 'area2', 'area3', 'area4' ]
        file = pd.read_csv( self.pathOfDataFolder + '/loadfuelareas/' + fileName, names=col_name )

        # 進行單位轉換，要*10，符合之前的資料 10^6 w
        file.iloc[:,1:5] = file.iloc[:,1:5].mul(10)

        # 產生新的 total load
        new_file = file[['date']].copy() 
        new_file['total_load'] = file.iloc[:,1:5].sum(axis=1) # 合併4個區域的總負載

        # 暫時存放檔案
        self.lastWeekLoad = new_file


class InputDataGenerator:

    def __init__( self,pathOfDataFolder, dateOfToday ):
        
        self.dateOfToday = dateOfToday + datetime.timedelta(days=1)
        self.dateForPred = dateOfToday + datetime.timedelta(days=2) # tomorrow of dateOfToday

        self.pathOfDataFolder = pathOfDataFolder

        self.BCG = BodyComfortGenerator(pathOfDataFolder=pathOfDataFolder,dateOfToday=dateOfToday)

        self.LDG = LoadGenerator(pathOfDataFolder=pathOfDataFolder,dateOfToday=dateOfToday)
    
    def autoRun(self):

        # 先產生天氣資料
        self.BCG.autoRun()

        # 再產生負載資料
        self.LDG.readInPredResult()
        self.LDG.createLastWeekLoad()

        # 合併兩者
        loadData = deepcopy(self.LDG.finalLoad)
        lastWeekData = deepcopy(list(self.LDG.lastWeekLoad['total_load']))
        bodyComfortData = deepcopy(self.BCG.finalBodyComfort)

        # 體感資料為 1 小時一筆 ，擴增為 10分鐘 一筆
        expendBDData = []
        for bdData in (list(bodyComfortData['Ta'])):
            for times in range(6):
                expendBDData.append( bdData )

        finalData = deepcopy(loadData)

        timeSeries = list( pd.date_range(start=self.dateOfToday, end=self.dateForPred, freq="10min"))[:-1]
        # print(timeSeries)
        finalData["date"] = timeSeries

        columnIndex = ['date','load']
        finalData=finalData.reindex(columns=columnIndex)

        finalData['bodyComfort'] = expendBDData
        finalData['lastWeek'] = lastWeekData

        finalData.to_csv( self.pathOfDataFolder + '/sample/sampleInputData_2.csv' )
        print("輸入資料產生完成")