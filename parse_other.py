import re
import csv

try:
    ff1 = open('Fri_Dec__6_14_38_14_CST_2019_other.txt', 'r')
    ff2 = open('Fri_Dec__6_14_38_14_CST_2019_other_parsed.csv', 'w')
    fr = csv.reader(ff1)
    fw = csv.writer((ff2))
except Exception:
    print("file open failed")
    exit()
iw_dic = {}
survey_dic = {}
queue_dic = {}
iw_timelist = []
survey_timelist = []
queue_timelist = []
for item in fr:
    # print(item[0])
    category = item[0]
    category = int(category)
    if category == 3:
        try:
            (IW, timex, mac_addr, station, device, signal) = item
        except Exception:
            print(item)
        station = station.strip(" ")
        if station == "60:02:b4:f9:8e:19":
            timex = int(timex)
            key = (category, timex)
            signal = float(signal)
            tmpw = [3, timex, signal]
            fw.writerow(tmpw)
            # iw_dic[key] = signal
            # iw_timelist.append(timex)
            continue
    if category == 6:
        try:
            (SURVEY, timex, mac_addr, time, time_busy, time_ext_busy,
             time_rx, time_tx, time_scan, center_freq, noise) = item
        except Exception:
            print(item)
        timex = int(timex)

        time = int(time)
        time_busy = int(time_busy)
        time_ext_busy = int(time_ext_busy)
        time_rx = int(time_rx)
        time_tx = int(time_tx)
        time_scan = int(time_scan)
        center_freq = int(center_freq)
        noise = float(noise)
        key = (category, timex)
        survey_dic[key] = [time, time_busy, time_rx, time_tx, time_scan, noise]
        survey_timelist.append(timex)
        continue
    if category == 4:
        try:
            (QUEUE, timex, mac_addr, queue_id, bytes1, packets, qlen,
             backlog, drops, requeues, overlimits) = item
        except Exception:
            print(item)
        timex = int(timex)

        key = (category, timex)
        bytes1 = int(bytes1)
        packets = int(packets)
        qlen = int(qlen)
        backlog = int(backlog)
        drops = int(drops)
        requeues = int(requeues)
        overlimits = int(overlimits)
        queue_dic[key] = [bytes1, packets, qlen,
                          backlog, drops, requeues, overlimits]
        queue_timelist.append(timex)
        continue
    else:
        # print(category)
        pass
# iw_timelist = sorted(iw_timelist, reverse=True)
survey_timelist = sorted(survey_timelist, reverse=True)
queue_timelist = sorted(queue_timelist, reverse=True)
# time_last = iw_timelist[0]
# print(iw_dic.keys())

# for item in iw_timelist:
#     key = (3, item)
#     iw_dic[key][0] = time_last
#     time_last = item
# # print(iw_dic[(3, iw_timelist[0])], iw_timelist[0])
# del iw_dic[(3, iw_timelist[0])]


window = 10000
length = len(survey_timelist)
for i in range(0, length):
    time_current = survey_timelist[i]
    k = 0
    dua = length - i
    found = False
    for j in range(1, dua):
        time_next = survey_timelist[j + i]
        duation = time_current - time_next
        if duation > window:
            found = True
            key_b = (6, time_current)
            key_e = (6, time_next)
            # print(survey_dic[key_b])
            (time_b, time_busy_b, time_rx_b, time_tx_b,
             time_scan_b, noise_b) = survey_dic[key_b]
            (time_e, time_busy_e, time_rx_e, time_tx_e,
             time_scan_e, noise_e) = survey_dic[key_e]
            ddd = float(time_b - time_e)
            if ddd == 0:
                continue
            time_busy_b = float(time_busy_b - time_busy_e) / ddd
            time_rx_b = float(time_rx_b - time_rx_b) / ddd
            time_tx_b = float(time_tx_b - time_tx_e) / ddd
            time_scan_b = float(time_scan_b - time_scan_e) / ddd
            time_middle = time_current / 2.0 + time_next / 2.0
            time_middle = round(time_middle)
            time_middle = int(time_middle)
            survey_dic[key_b] = [time_middle, time_busy_b,
                                 time_rx_b, time_tx_b, time_scan_b, noise_b]
            tmpw = [6, time_current, time_middle, time_busy_b,
                    time_rx_b, time_tx_b, time_scan_b, noise_b]
            fw.writerow(tmpw)
            break
    if found is False:
        print(i, length)
        key = (6, time_current)
        del survey_dic[key]
print(len(survey_dic))
length = len(queue_timelist)
for i in range(0, length):
    time_current = queue_timelist[i]
    k = 0
    dua = length - i
    found = False
    for j in range(1, dua):
        time_next = queue_timelist[j + i]
        duation = time_current - time_next
        if duation > window:
            found = True
            key_b = (4, time_current)
            key_e = (4, time_next)
            # print(queue_dic[key_b])
            (bytes1_b, packets_b, qlen_b, backlog_b, drops_b,
             requeues_b, overlimits_b) = queue_dic[key_b]
            (bytes1_e, packets_e, qlen_e, backlog_e, drops_e,
             requeues_e, overlimits_e) = queue_dic[key_e]
            ddd = float(time_current - time_next)
            if ddd == 0:
                continue
            bytes1_b = float(bytes1_b - bytes1_e) / ddd
            packets_b = float(packets_b - packets_e) / ddd
            drops_b = float(drops_b - drops_e) / ddd
            requeues_b = float(requeues_b - requeues_e) / ddd
            overlimits_b = float(overlimits_b - overlimits_e) / ddd
            time_middle = time_current / 2.0 + time_next / 2.0
            time_middle = round(time_middle)
            time_middle = int(time_middle)
            queue_dic[key_b] = [time_middle, bytes1_b, packets_b,
                                qlen_b, backlog_b, drops_b,
                                requeues_b, overlimits_b]
            tmpw = [4, time_current, time_middle, bytes1_b, packets_b,
                    qlen_b, backlog_b, drops_b, requeues_b, overlimits_b]
            fw.writerow(tmpw)
            break
    if found is False:
        print(i, length)
        key = (4, time_current)
        del queue_dic[key]
print(len(queue_dic))

if ff1:
    ff1.close()
if ff2:
    ff2.close()
