from InputDataGenerator import InputDataGenerator
import datetime
from datetime import timedelta
"""
in future(while actual using), the "dateOfToday" will be datetime.today()
"""

GNT = InputDataGenerator( pathOfDataFolder = '../data',
                          dateOfToday = datetime.date(2021, 7, 3))

GNT.autoRun()
