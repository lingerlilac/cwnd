import re
import csv
import matplotlib.pyplot as plt

try:
    ff1 = open('Fri_Dec__6_14_38_12_CST_2019_winsize.txt', 'r')
    fr = csv.reader(ff1)
except Exception:
    print("file open failed")
    exit()
winsize_list = []
sequence_last = -1
ack_list = []
timelist = []
timelist1 = []
ack_sequence_last = -1
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
    if ip_src == '192.168.11.103':
        winsize_list.append(sequence)
        if (sequence - sequence_last) < -1000000:
            print(sequence_last, sequence, timex)
        sequence_last = sequence
        timelist.append(timex)
    if ip_src == '192.168.11.109':
        ack_list.append(ack_sequence)
        timelist1.append(timex)
        # if abs(ack_sequence - ack_sequence_last) > 10000000:
        #     print(ack_sequence_last, ack_sequence, timex, sequence, 'aaa')
        ack_sequence_last = ack_sequence
plt.plot(timelist, winsize_list, label='sequence')
plt.plot(timelist1, ack_list, label='ack_sequence')
plt.legend()
plt.show()
if ff1:
    ff1.close()
