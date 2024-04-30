from datetime import datetime, timedelta
obj = datetime.now()
date = obj.date()
print(date)
time = obj.strftime('%X')
print(time)
print(date - timedelta(30))