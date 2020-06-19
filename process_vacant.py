import csv

try:
    f1 = open('dataset.csv', 'r')
    f2 = open('dataset_n.csv', 'w', newline='')
    fr = csv.reader(f1)
    fw = csv.writer(f2)
except Exception:
    print('file open failed')
    exit()
for i in fr:
    if len(i) == 0:
        continue
    fw.writerow(i)
if f1:
    f1.close()
if f2:
    f2.close()
