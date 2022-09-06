import pandas as pd

DailyTempMean = {}


#讀取單一檔案
data = pd.read_csv('/Users/hsiehyuanlung/Desktop/氣象資料/1998-2018局屬/局屬2018All.csv')#讀取資料
#print(data)
data = data[data['站碼'].astype(str).str.contains('46692')]  #篩選測站id
data = data[data['資料時間'].astype(str).str.endswith(('00','06','12','18'))]    #篩選四個時間
data = data[['站碼','資料時間','氣溫(度)']]    #篩選出指定欄
data = data.drop(data[data['氣溫(度)']<0].index)    #刪除<0的溫度資料
data['資料時間'] = data['資料時間'] // 100


DailyTemp = []
DailyTempMean = {}
data = data.append({'站碼':99999,'資料時間':99999999,'氣溫(度)':-999},ignore_index=True)  #增加最後一行終止行，計算日均溫時出錯
for i in range(len(data)-1):    
    if data.iat[i,2] >0:    #如果本日均溫大於零度(避免無數據(記錄為-9999)造成影響)
        DailyTemp.append(data.iat[i,2]) #將此時段氣溫存進DailyTemp中
    if (data.iat[i,1]) != (data.iat[i+1,1]):    #如果日期和下一筆數據不同(為此日最後一筆數據)
        if len(DailyTemp) >0:   #若一天四時段皆無數據，則不計入日均溫
            day_mean = sum(DailyTemp) / len(DailyTemp)  #計算日均溫
            DailyTempMean[str(data.iat[i,1])] = day_mean    #將日均溫存進DailyTempMean中
        DailyTemp.clear() 

#print(DailyTempMean)
DailyTempMean = sorted(DailyTempMean.items(),key = lambda x:x[0])   #將資料由小到大(按日期)排序 items將DailyTempMeanionary轉為tuple型態
DailyTempMeanDataFrame = pd.DataFrame(DailyTempMean,columns=['Date', 'Mean TEMP']) #將DailyTempMean轉為DataFrame
#print(DailyTempMeanDataFrame)
#DailyTempMeanDataFrame.to_csv('2008-2018DailyTemp.csv') #輸出日均溫資料，可用 index = False 不輸出索引



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
WeeklyTempMeanDataFrame.to_csv('局屬2018WeeklyTemp.csv') #輸出週均溫資料，可用 index = False 不輸出索引


'''
for i in range(len(DailyTempMean)):
    date = int(DailyTempMean[i][0]) % 100
    if date == 1 or date == 8 or date == 15 or date == 22:
        if len(WeeklyTemp) >= 1:  #避免1/1多餘運算
            mean = sum(WeeklyTemp) / len(WeeklyTemp)    #計算週均溫(每週以1,8,15,22號開始)
            week = (int(str(DailyTempMean[i][0])[4:6])-1) * 4 + ((date-1)//7)   #週數=(月份-1)x4+((日期-1)/7)+1 -1 (要-1因為計算的是前一週的週均溫)
            WeeklyTempMean[+str('%02d' % week)] = mean   #將週均溫儲存在WeeklyTempMean中
            WeeklyTemp.clear()        #清空此星期的氣溫數據
    if DailyTempMean[i][1] >= 5:    #如果本日均溫大於十度(避免無數據(記錄為-9999)造成影響)
        WeeklyTemp.append(DailyTempMean[i][1]) #將本日均溫儲存進WeeklyTemp中
'''