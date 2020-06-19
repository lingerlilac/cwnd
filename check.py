import csv

try:
    fr = csv.reader(open('tmp.csv', 'r'))
except Exception:
    print('file open failed')
    exit()

xdic = {}

for item in fr:
    (timex, seq, ack) = item
    try:
        xdic[seq].add(ack)
    except:
        xdic[seq] = set()
        xdic[seq].add(ack)
print(xdic)
print("------------------------------")
for key in xdic.keys():
    if len(xdic[key]) > 1:
        print(key, xdic[key])
print(len(xdic))
