import csv
import numpy as np

try:
    file0 = open('df.csv', 'r')
    file1 = open('dff.csv', 'w', newline='')
    fr = csv.reader(file0)
    fw = csv.writer(file1)
except Exception:
    print('df or dff open failed')
    exit()
names = []
for i in fr:
    names = i
    break
print(names)
last_5 = [-1.0 for i in range(0, 5)]
count = 0
fw.writerow(names)
for item in fr:
    (signal, time_busy_b, time_tx_b, noise_b, packets_b, una,
     ret, window) = [float(item[i]) for i in range(0, len(item))]
    
    if min(last_5) < 0:
        last_5[last_5.index(min(last_5))] = una
        continue
    # print(last_5, count)
    if (una - np.mean(last_5)) > 100:
        count += 1
        # print(item)
        continue
    last_5[last_5.index(min(last_5))] = una
    fw.writerow(item)
    # break
print(count)
if file0:
    file0.close()
if file1:
    file1.close()
