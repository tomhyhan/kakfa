from datetime import datetime, timedelta
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print((datetime.now()+timedelta(seconds=5)).strftime("%Y-%m-%d %H:%M:%S"))
