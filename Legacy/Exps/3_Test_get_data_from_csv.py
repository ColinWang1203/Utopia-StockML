import pandas
df = pandas.read_csv('20191125.csv', encoding = 'big5', skiprows=186, usecols = [0,*range(5, 9)])
print(df)