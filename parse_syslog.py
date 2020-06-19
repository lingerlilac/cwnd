import re
import csv

try:
    ff1 = open('syslog3', 'r')
    ff2 = open('parsed_syslog3.csv', 'w')
    fr = csv.reader(ff1)
    fw = csv.writer((ff2))
except Exception:
    print("file open failed")
    exit()
for item in fr:
    x = str(item)
    if x.find('shadowsocks') >= 0:
        continue
    item1 = item[0]
    index1 = item1.find(']')
    string = item1[index1 + 1:]
    string = re.split(',', string)[0]
    try:
        string = int(string)
    except:
        # print(string)
        continue
    # print(string)
    sec = string
    usec = item[1]
    usec = int(usec)
    cwnd = int(item[2])
    nxt = int(item[3])
    una = int(item[4])
    timee = sec * 1000000 + usec
    # print(timee, cwnd, nxt, una)
    fw.writerow((timee, cwnd, nxt, una))

if ff1:
    ff1.close()
if ff2:
    ff2.close()
