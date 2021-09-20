from InputDataGenerator import InputDataGenerator
import datetime
from datetime import timedelta
"""
in future(while actual using), the "dateOfToday" will be datetime.today()
"""

GNT = InputDataGenerator( pathOfDataFolder = '/home/g22qkqkq/load-forecast/data',dateOfToday = datetime.date.today()-timedelta(days=1))
GNT.autoRun()
with open('dateInfo.txt','a') as outFile:
    outFile.write('\n' + str(datetime.datetime.now()))
