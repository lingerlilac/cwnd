import csv

try:
    ff1 = open('dataset.csv', 'r')
    fr1 = csv.reader(ff1)
except Exception:
    print('dataset.csv openfailed')
    exit()
X = []
y = []
vaule_dic = {}
for item in fr1:
    (signal, time_busy_b, time_rx_b, time_tx_b, time_scan_b,
     noise_b, bytes1_b, packets_b, qlen_b, backlog_b, drops_b,
     requeues_b, overlimits_b, una, window) = [float(item[i]) for i in range(1, len(item))]
    # X.append([una, signal, time_busy_b, time_rx_b, time_tx_b, time_scan_b,
    #  noise_b, bytes1_b, packets_b, qlen_b, backlog_b, drops_b,
    #  requeues_b, overlimits_b])
    try:
        vaule_dic[una] += 1
    except Exception:
        vaule_dic[una] = 1
keys = vaule_dic.keys()
keys = sorted(keys)
for key in keys:
    print(key, vaule_dic[key])
