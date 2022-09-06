import pandas as pd
import os

path = '/Users/hsiehyuanlung/Desktop/氣象資料/2019 局屬/2019All'
allFileList = os.listdir(path)

DailyTempMean = {}

#讀取檔案夾內所有檔案
for file in allFileList:
    if not file.startswith('.DS_Store') and os.path.join(path,file):    #不讀取'.DS_Store' 檔案
        data = pd.read_csv(os.path.join(path,file)) #逐個讀取檔案夾內資料
        data = data[data['station_id'].astype(str).str.contains('466920')]  #篩選測站id
        #data = data[data['obsTime'].str.contains('00:00:00|06:00:00|12:00:00|18:00:00')]    #篩選四個時間
        data = data[['station_id','obsTime','TEMP']]    #篩選出指定欄
        data = data.drop(data[data['TEMP']<0].index)    #刪除<0的溫度資料
        #print(data)

        mean_data = data['TEMP'].mean() #計算TEMP欄的平均
        print('Date : ' + file[6:14] + '    ' + str(mean_data))
        DailyTempMean[file[6:14]] = mean_data    #將資料儲存在DailyTempMean中


DailyTempMean = sorted(DailyTempMean.items(),key = lambda x:x[0]) #將資料由小到大(按日期)排序 items將DailyTempMeanionary轉為tuple
print(DailyTempMean)
DailyTempMeanDataFrame = pd.DataFrame(DailyTempMean,columns=['Date', 'Mean TEMP']) #將DailyTempMean轉為DataFrame
#print(DailyTempMeanDataFrame)
#DailyTempMeanDataFrame.to_csv('2019DailyTemp.csv') #輸出日均溫資料，可用 index = False 不輸出索引

WeeklyTemp = []
WeeklyTempMean = {}
week = 1    #從第一週開始
for i in range(len(DailyTempMean)):
    datei = int(DailyTempMean[i][0]) % 100
    if datei == 1 or datei == 8 or datei == 15 or datei == 22:
        for j in range(i,i+10):
            if j < len(DailyTempMean):
                datej = int(DailyTempMean[j][0]) % 100
                if (datej != datei) and (datej == 1 or datej == 8 or datej == 15 or datej == 22):
                    break
                if DailyTempMean[j][1] >= 5:
                    WeeklyTemp.append(DailyTempMean[j][1])
        if len(WeeklyTemp) > 0:    #若一週皆無數據，則不計入週均溫
            mean = sum(WeeklyTemp) / len(WeeklyTemp)    #計算週均溫(每週以1,8,15,22號開始)
            week = (int(str(DailyTempMean[i][0])[4:6])-1) * 4 + ((datei-1)//7)+1   #週數=(月份-1)x4+((日期-1)/7)+1 
            WeeklyTempMean[(str(DailyTempMean[i][0])[0:8]+'%02d' % week)] = mean   #將週均溫儲存在WeeklyTempMean中 
        else:    #若一週皆無數據，則該週記為0
            week = (int(str(DailyTempMean[i][0])[4:6])-1) * 4 + ((datei-1)//7)+1   #週數=(月份-1)x4+((日期-1)/7)+1
            WeeklyTempMean[(str(DailyTempMean[i][0])[0:8]+'%02d' % week)] = 0   #無資料則記為0
        WeeklyTemp.clear()        #清空此星期的氣溫數據


#print(WeeklyTempMean)

WeeklyTempMeanDataFrame = pd.DataFrame(WeeklyTempMean.items(),columns=['Week', 'Mean TEMP'])
print(WeeklyTempMeanDataFrame)
WeeklyTempMeanDataFrame.to_csv('局屬2019WeeklyTemp.csv') #輸出週均溫資料，可用 index = False 不輸出索引


'''
#讀取單一檔案
data = pd.read_csv('/Users/hsiehyuanlung/Desktop/氣象資料/2019/2019All/auto_20190430.csv')   #讀取資料
data = data[data['station_id'].str.contains('C0A880')]  #篩選測站id
data = data[data['obsTime'].str.contains('00:00:00|06:00:00|12:00:00|18:00:00')]    #篩選四個時間
data = data[['station_id','obsTime','TEMP']]    #篩選出指定欄
print(data)
'''

