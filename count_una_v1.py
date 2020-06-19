import re
import csv

try:
    ff1 = open('Fri_Dec__6_14_38_12_CST_2019_winsize_parsed.csv', 'r')
    ff2 = open('una.csv', 'w', newline='')
    ff3 = open('debug.csv', 'w', newline='')
    fr = csv.reader(ff1)
    fw = csv.writer((ff2))
    ft = csv.writer((ff3))
except Exception:
    print("file open failed")
    exit()
datalist = []
timelist103 = []
for item in fr:
    try:
        (timex, ip_src, sequence, ack_sequence,
         datalength, sourceaddr, destination) = item
    except Exception:
        # print(item, 'ass')
        continue
    timex = int(timex)
    timelist103.append(timex)
    datalist.append([timex, ip_src, sequence, ack_sequence,
                     datalength, sourceaddr, destination])
timelist103 = sorted(timelist103)
timelist103dic = {}

for i in range(0, len(timelist103)):
    timelist103dic[timelist103[i]] = i
unacked = []
dic_103 = {}
dic_109 = {}
data_obtained = []

lastseq103 = -1
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
        lastseq103 = timex
        if datalength == 0:
            continue
        else:
            index = timelist103dic[timex]
            try:
                ret = dic_103[sequence][2] + 1
                dic_103[sequence] = [index, timex, ret, ack_sequence]
            except:
                dic_103[sequence] = [index, timex, 0, ack_sequence]
    if ip_src == "192.168.11.109":

        try:
            if lastseq103 == -1:
                continue
            index = timelist103dic[lastseq103]
            # print("ack_sequence", timex)
            dic_109[ack_sequence] = [index, timex, sequence, ack_sequence]

            # dic_109[ack_sequence].append([i, timex, sourceaddr, destination])
        except:
            if lastseq103 == -1:
                continue
            index = timelist103dic[lastseq103]
            # print("ack_sequence", timex)
            dic_109[ack_sequence] = [index, timex, sequence, ack_sequence]
print(len(dic_103), len(dic_109))
for key in dic_109.keys():
    (indey, timey, sourceaddr, destination) = dic_109[key]
    try:
        (index, timex, sourceaddr1, destination1) = dic_103[key]
        count = indey - index
        # print(indey, index)
        # data_obtained.append([timex, count])
        fw.writerow([timex, count, sourceaddr1])
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
