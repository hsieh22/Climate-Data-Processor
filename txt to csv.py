import csv
data = []
with open('/Users/hsiehyuanlung/Desktop/氣象資料/1998-2018局屬/Metro_1998-2017_467050.txt') as f:
    for line in f:
        print(line)
        temp = line.split()
        data.append(temp)
print(data)

# 開啟輸出的 CSV 檔案
with open('output.csv', 'w', newline='') as csvfile:
  # 建立 CSV 檔寫入器
  writer = csv.writer(csvfile)
  # 寫入一列資料
  for i in range(len(data)):
    writer.writerow(data[i])
