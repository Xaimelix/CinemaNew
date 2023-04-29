import datetime

a = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d')
b = a + datetime.timedelta(days=1)
b.strftime('%Y-%m-%d')
