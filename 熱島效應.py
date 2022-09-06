import pandas as pd


#讀取單一檔案
DATA = pd.read_csv('/Users/hsiehyuanlung/Desktop/氣象資料/1998-2018 自動/2008-2018.csv')   #讀取資料

#DATA['yyyymmddhh'] = DATA['yyyymmddhh'] // 100  #時間欄只保留日期
DATA = DATA[['#stno','yyyymmddhh','TX01']]    #篩選出指定欄   # #stno站碼 TX01氣溫(度)
DATA = DATA.drop(DATA[DATA['TX01']<0].index)    #刪除<0的溫度資料

location = ['C0C480','C0C520','C0C490','C0C620','C0C640','C0C680','C0C590','C0C630','C0C610','C0C670','C0C650','C0C660','C0C570','C0C540']
time = ['2018122106','2018122112','2018122118','2018122124']    #欲篩選的時間    #yyyymmddhh資料時間 3/20,6/21,9/23,12/21 
#台北 'C0A9E0','C0A9C0','CM0020','C0A980','C0AH40','C0A9A0','C0A9F0','C0AC80','C0AI40','C0A9B0','C0AC40','C0AC70','C0A9G0','C0AH70','CAA040','CAA090'
#桃園 'C0C480','C0C520','C0C490','C0C620','C0C640','C0C680','C0C590','C0C630','C0C610','C0C670','C0C650','C0C660','C0C570','C0C540'
#時間 '032106','032112','032118','032124','062106','062112','062118','062124','092106','092112','092118','092124','122106','122112','122118','122124'
'''
桃園C0C480
中壢C0C520
八德C0C490
蘆竹C0C620
龜山C0C640
龜山C0C680
觀音C0C590
大溪C0C630
龍潭C0C610
龍潭C0C670
平鎮C0C650
楊梅C0C660
新屋C0C570
大園C0C540
'''

WOW = pd.DataFrame()

def calculate(a,b):
    global WOW
    print(a)
    print(b)
    DailyTemp = {}
    data = DATA[DATA['#stno'].astype(str).str.contains(b)]  #篩選測站id
    data = data[data['yyyymmddhh'].astype(str).str.endswith(a)]    #篩選四個時間   #yyyymmddhh資料時間 
    for i in range(len(data)):    
        DailyTemp[str(data.iat[i,1])] = data.iat[i,2]    #將日均溫存進DailyTemp中

    DailyTemp = sorted(DailyTemp.items(),key = lambda x:x[0])   #將資料由小到大(按日期)排序 items將DailyTempMeanionary轉為tuple型態
    DailyTempDataFrame = pd.DataFrame(DailyTemp,columns=['Date', b]) #將DailyTempMean轉為DataFrame
    DailyTempDataFrame = DailyTempDataFrame.set_index(['Date'])   #將Week欄設為索引
    print(DailyTempDataFrame)
    WOW = pd.concat([WOW,DailyTempDataFrame],axis = 1)



for i in range(len(time)):
    #print(time[i])
    for j in range(len(location)):
        #print(location[j])
        calculate(time[i],location[j])
    #WOW = pd.concat(WeeklyMeanDataFrame)

print(WOW)
WOW.to_csv('2018冬至桃園熱島.csv') #輸出週均溫資料，可用 index = False 不輸出索引
