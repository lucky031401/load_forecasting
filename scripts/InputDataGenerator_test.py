from InputDataGenerator import InputDataGenerator
import datetime
from datetime import timedelta
"""
in future(while actual using), the "dateOfToday" will be datetime.today()
"""

GNT = InputDataGenerator( pathOfDataFolder = '../data',
                          dateOfToday = datetime.date.today()-timedelta(days=1))

GNT.autoRun()
