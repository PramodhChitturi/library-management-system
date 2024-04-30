from datetime import datetime, timedelta
a = datetime.now()
print(a.date())
print(a.strftime('%X'))
b = a - timedelta(days = 7)
print(b)
print(b.date())
print(b.strftime('%X'))