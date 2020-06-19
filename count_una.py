import re
import csv

try:
    ff1 = open('Fri_Dec__6_14_38_12_CST_2019_winsize_parsed.csv', 'r')
    ff2 = open('una.csv', 'w')
    ff3 = open('debug.csv', 'w')
    fr = csv.reader(ff1)
    fw = csv.writer((ff2))
    ft = csv.writer((ff3))
except Exception:
    print("file open failed")
    exit()
datalist = []
for item in fr:
    try:
        (timex, ip_src, sequence, ack_sequence,
         datalength, sourceaddr, destination) = item
    except Exception:
        # print(item, 'ass')
        continue
    datalist.append([timex, ip_src, sequence, ack_sequence,
                     datalength, sourceaddr, destination])

unacked = []
dic_103 = {}
dic_109 = {}
data_obtained = []
for i in range(0, len(datalist)):
    (timex, ip_src, sequence, ack_sequence,
     datalength, sourceaddr, destination) = datalist[i]
    datalength = int(datalength)
    sequence = int(sequence)
    ack_sequence = int(ack_sequence)
    sourceaddr = int(sourceaddr)
    destination = int(destination)
    timex = int(timex)
    if ip_src == "192.168.11.103":
        if datalength == 0:
            continue
        else:
            dic_103[sequence] = [i, timex, sourceaddr, destination]
    if ip_src == "192.168.11.109":
        dic_109[ack_sequence] = [i, timex, sourceaddr, destination]

for key in dic_109.keys():
    (indey, timey, sourceaddr, destination) = dic_109[key]
    try:
        (index, timex, sourceaddr1, destination1) = dic_103[key]
        count = indey - index
        # print(indey, index)
        # data_obtained.append([timex, count])
        fw.writerow([timex, count])
        ft.writerow([timex, key, index, indey, sourceaddr,
                     destination, sourceaddr1, destination1])
    except:
        continue
print(data_obtained)
if ff1:
    ff1.close()
if ff2:
    ff2.close()
if ff3:
    ff3.close()
