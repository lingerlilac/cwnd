import re
import csv

try:
    ff1 = open('Fri_Dec__6_14_38_12_CST_2019_winsize.txt', 'r')
    ff2 = open('Fri_Dec__6_14_38_12_CST_2019_winsize_parsed.csv', 'w')
    fr = csv.reader(ff1)
    fw = csv.writer((ff2))
except Exception:
    print("file open failed")
    exit()
for item in fr:
    try:
        (WINSIZE, timex, mac_addr,
         ip_src, ip_dst, sourceaddr, destination,
         sequence, ack_sequence, windowsize,
         cal_windowsize, datalength, flags, kind,
         length, wscale) = item
    except Exception:
        print(item)
        continue
    sequence = int(sequence)
    ack_sequence = int(ack_sequence)
    datalength = int(datalength)
    sourceaddr = int(sourceaddr)
    destination = int(destination)
    if sourceaddr not in (10002, 52098):
        continue
    if destination not in (10002, 52098):
        continue
    ip_src = ip_src.strip(' ')
    if ip_src not in ("192.168.11.103", "192.168.11.109"):
        # print(ip_src)
        continue
    if ack_sequence == 0:
        continue
    if sequence == 0:
        continue
    # print(sequence, ack_sequence)
    timex = int(timex)
    fw.writerow((timex, ip_src, sequence, ack_sequence,
                 datalength, sourceaddr, destination))
    # break

if ff1:
    ff1.close()
if ff2:
    ff2.close()
