import pandas as pd
import re

data = pd.read_csv('E:/problem2/result10.csv', engine='python')

data1={}

data1['zone'] = data['address'].str.split('-').str[0]
data1['location'] = data['address'].str.split('-').str[1]
data1['village'] = data['address'].str.split('-').str[2]

data1['area'] = []
for item in data['area'].values:
    x=re.findall('(\d+)',item)
    data1['area'].append(int(re.findall('(\d+)',item)[0]))

data1['direction'] = data['direction']

temp = []
for item in data['huxing'].values:
    temp.append(re.findall('(\d+)',item))

data1['room'],data1['hall'],data1['wc'] = [],[],[]
for x in temp:
    if len(x)==3:
        data1['room'].append(x[0])
        data1['hall'].append(x[1])
        data1['wc'].append(x[2])
    else:
        data1['room'].append('')
        data1['hall'].append('')
        data1['wc'].append('')

data1['height'] = data['floor'].str[0]
data1['floor'] = []
for item in data['floor'].values:
    if len(item)>3:
        data1['floor'].append(int(re.findall('(\d+)',item)[0]))
    else:
        data1['floor'].append('')

data1['publish'] = data['publish']

data1['subway'] = []
data1['beauty'] = []
i=1
for x in data['remark'].values:
    if type(x) is str:
        data1['subway'].append(bool('近地铁' in x))
        data1['beauty'].append(bool('精装' in x))
    else:
        data1['subway'].append('')
        data1['beauty'].append('')
    i+=1
    print(i)
data1['house_price'] = data['price']
data1['ave_price']=data1['house_price']/data1['area']

pd.DataFrame(data1).to_csv('result.csv',encoding='gbk')
