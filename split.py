import csv
from sklearn.model_selection import train_test_split
try:
    ff1 = open('dataset.csv', 'r')
    fr1 = csv.reader(ff1)
except Exception:
    print('dataset.csv openfailed')
    exit()
X = []
y = []
for item in fr1:
    attr = item
    break
attr = ["Id", "una", "ret", "signal", "time_busy_b", "time_rx_b",
        "time_tx_b", "time_scan_b", "noise_b",
        "bytes1_b", "packets_b", "qlen_b", "backlog_b", "drops_b",
        "requeues_b", "overlimits_b", "SalePrice"]
attr1 = ["Id", "una", "ret", "signal", "time_busy_b", "time_rx_b",
         "time_tx_b", "time_scan_b", "noise_b",
         "bytes1_b", "packets_b", "qlen_b", "backlog_b", "drops_b",
         "requeues_b", "overlimits_b"]

# length = len(attr)
# x_attr = attr[:length - 1]
# y_attr = attr[length - 1: ]
for item in fr1:
    (signal, time_busy_b, time_rx_b, time_tx_b, time_scan_b,
     noise_b, bytes1_b, packets_b, qlen_b, backlog_b, drops_b,
     requeues_b, overlimits_b, una, ret,
     window) = [float(item[i]) for i in range(1, len(item))]
    X.append([una, ret, signal, time_busy_b, time_rx_b, time_tx_b, time_scan_b,
              noise_b, bytes1_b, packets_b, qlen_b, backlog_b, drops_b,
              requeues_b, overlimits_b])
    y.append(window)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3)
try:
    ff2 = open('train.csv', 'w')
    ff3 = open('test.csv', 'w')
    ff4 = open('test_y.csv', 'w')
    fw2 = csv.writer(ff2)
    fw3 = csv.writer(ff3)
    fw4 = csv.writer(ff4)
except Exception:
    print('file open failed')
    exit()
fw2.writerow(attr)
fw3.writerow(attr1)
attr = ["SalePrice"]
fw4.writerow(attr)

length = len(X_train)
for i in range(0, length):
    tmp = X_train[i]
    tmp1 = y_train[i]
    tmp = [i] + tmp + [tmp1]
    fw2.writerow(tmp)
length = len(X_test)
for i in range(0, length):
    tmp = X_test[i]
    tmp1 = y_test[i]
    tmp = [i] + tmp
    fw4.writerow([tmp1])
    fw3.writerow(tmp)
if ff2:
    ff2.close()
if ff3:
    ff3.close()
