import re
import csv
import gc
import matplotlib.pyplot as plt
try:
    ff1 = open('Fri_Dec__6_14_38_12_CST_2019_winsize_parsed.csv', 'r')
    ff2 = open('xxx.csv', 'w', newline='')
    fr = csv.reader(ff1)
    fw = csv.writer((ff2))
except Exception:
    print("file open failed")
    exit()
timelistsrc = []
timelistdst = []
sequencelist = []
ack_sequencelist = []
for item in fr:
    try:
        (timex, ip_src, sequence, ack_sequence,
            datalength, sourceaddr, destination) = item
    except Exception:
        # print(item)
        continue
    sequence = int(sequence)
    ack_sequence = int(ack_sequence)
    timex = int(timex)
    if timex >= 1575615769573851 and timex < 1575617531083915:
        if ip_src == '192.168.11.103':
            sequence += 4294966614
        elif ip_src == '192.168.11.109':
            ack_sequence += 4294966614
    elif timex >= 1575617531083915 and timex < 1575619758653760:
        if ip_src == '192.168.11.103':
            sequence += (4294966614 + 4294967142)
        elif ip_src == '192.168.11.109':
            ack_sequence += (4294966614 + 4294967142)
    elif timex >= 1575619758653760 and timex < 1575622409075240:
        if ip_src == '192.168.11.103':
            sequence += (4294966614 + 4294967142 + 4294966222)
        elif ip_src == '192.168.11.109':
            ack_sequence += (4294966614 + 4294967142 + 4294966222)
    elif timex >= 1575622409075240 and timex < 1575624451748626:
        if ip_src == '192.168.11.103':
            sequence += (4294966614 + 4294967142 + 4294966222 + 4294966750)
        elif ip_src == '192.168.11.109':
            ack_sequence += (4294966614 + 4294967142 + 4294966222 + 4294966750)
    elif timex >= 1575624451748626:
        if ip_src == '192.168.11.103':
            sequence += (4294966614 + 4294967142 +
                         4294966222 + 4294966750 + 4294967278)
        elif ip_src == '192.168.11.109':
            ack_sequence += (4294966614 + 4294967142 +
                             4294966222 + 4294966750 + 4294967278)
    if ip_src == '192.168.11.103':
        sequencelist.append(sequence)
        timelistsrc.append(timex)
    if ip_src == '192.168.11.109':
        ack_sequencelist.append(ack_sequence)
        timelistdst.append(timex)

    fw.writerow((timex, ip_src, sequence, ack_sequence,
                 datalength, sourceaddr, destination))
plt.plot(timelistsrc, sequencelist, label='sequence')
plt.plot(timelistdst, ack_sequencelist, label='ack_sequence')
plt.legend()
plt.show()

if ff1:
    ff1.close()
if ff2:
    ff2.close()
gc.collect()
