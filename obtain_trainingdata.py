import re
import csv
import gc

try:
    ff1 = open('Fri_Dec__6_14_38_14_CST_2019_other_parsed.csv', 'r')
    ff3 = open('una.csv', 'r')
    ff2 = open('dataset.csv', 'w', newline='')
    ff4 = open('parsed_syslog3.csv', 'r')
    ft = csv.reader(ff4)
    fr = csv.reader(ff1)
    fw = csv.writer((ff2))
    fs = csv.reader(ff3)
except Exception:
    print("file open failed")
    exit()


iwdata = []
surveydata = []
queuedata = []
windowdata = []
for item in fr:
    # print(item[0])
    category = item[0]
    category = int(category)
    if category == 3:
        try:
            (categ, timex, signal) = item
        except Exception:
            print(item, "ss")
            break
        categ = int(categ)
        timex = int(timex)
        signal = float(signal)
        # print(categ, timex, signal)
        iwdata.append([timex, signal])
        continue
    if category == 6:
        try:
            (categ, time_current, time_middle, time_busy_b,
             time_rx_b, time_tx_b, time_scan_b, noise_b) = item
        except Exception:
            print(item)
        categ = int(categ)
        time_current = int(time_current)
        time_middle = int(time_middle)
        time_busy_b = float(time_busy_b)
        time_rx_b = float(time_rx_b)
        time_tx_b = float(time_tx_b)
        time_scan_b = float(time_scan_b)
        noise_b = float(noise_b)
        surveydata.append([time_current, time_middle, time_busy_b,
                           time_rx_b, time_tx_b, time_scan_b, noise_b])
        continue
    if category == 4:
        try:
            (categ, time_current, time_middle, bytes1_b, packets_b,
             qlen_b, backlog_b, drops_b, requeues_b, overlimits_b) = item
        except Exception:
            print(item)
        time_current = int(time_current)
        time_middle = int(time_middle)
        bytes1_b = float(bytes1_b)
        packets_b = float(packets_b)
        qlen_b = int(qlen_b)
        backlog_b = int(backlog_b)
        drops_b = float(drops_b)
        requeues_b = float(requeues_b)
        overlimits_b = float(overlimits_b)
        queuedata.append([time_current, time_middle, bytes1_b, packets_b,
                          qlen_b, backlog_b, drops_b,
                          requeues_b, overlimits_b])
        continue
    else:
        # print(category)
        pass
# print(len(iwdata), len(surveydata), len(queuedata))
for item in fs:
    try:
        (timex, count, retrans) = item
    except Exception:
        continue
    timex = int(timex)
    count = int(count)
    retrans = int(retrans)
    ret = 0
    if retrans > 1:
        ret = 1
    windowdata.append([timex, count, ret])
# print(len(windowdata))
tmplist = iwdata + surveydata
tmplist = sorted(tmplist)
print(len(tmplist), len(iwdata), len(surveydata))
iwsurvey = []
iw_last = []
for item in tmplist:
    try:
        (timex, signal) = item
        iw_last = [timex, signal]
    except Exception:
        (time_current, time_middle, time_busy_b,
         time_rx_b, time_tx_b, time_scan_b, noise_b) = item
        survey = [time_busy_b, time_rx_b, time_tx_b, time_scan_b, noise_b]
        if len(iw_last) > 0:
            iwsurvey.append(iw_last + survey)
            iw_last = []
del tmplist
gc.collect()
tmplist = iwsurvey + queuedata
tmplist = sorted(tmplist)
# print("sss", len(tmplist))
iwsurveyqueue = []
is_last = []
for item in tmplist:
    try:
        (timex, signal, time_busy_b, time_rx_b,
         time_tx_b, time_scan_b, noise_b) = item
        is_last = [timex, signal, time_busy_b,
                   time_rx_b, time_tx_b, time_scan_b, noise_b]
    except Exception:
        (time_current, time_middle, bytes1_b, packets_b, qlen_b,
         backlog_b, drops_b, requeues_b, overlimits_b) = item
        tmp = [bytes1_b, packets_b, qlen_b, backlog_b,
               drops_b, requeues_b, overlimits_b]
        if len(is_last) > 0:
            iwsurveyqueue.append(is_last + tmp)
            is_last = []
del iwsurvey
gc.collect()
# print(iwsurveyqueue)
# print(len(iwsurveyqueue))


tmplist = iwsurveyqueue + windowdata
tmplist = sorted(tmplist)
print("sss", len(tmplist))
iwsurveyqueuewindow = []
is_last = []
for item in tmplist:
    # print(len(item))
    try:
        (timex, signal, time_busy_b, time_rx_b,
            time_tx_b, time_scan_b, noise_b,
         bytes1_b, packets_b, qlen_b, backlog_b,
         drops_b, requeues_b, overlimits_b) = item
        is_last = [timex, signal, time_busy_b, time_rx_b,
                   time_tx_b, time_scan_b, noise_b,
                   bytes1_b, packets_b, qlen_b,
                   backlog_b, drops_b, requeues_b, overlimits_b]
    except Exception:
        (time1, count, ret) = item
        if count < 0:
            continue
        ret = int(ret)
        tmp = [count, ret]
        if len(is_last) > 0:
            iwsurveyqueuewindow.append(is_last + tmp)
            # fw.writerow(is_last + tmp)
            is_last = []

del iwsurveyqueue
gc.collect()
wdata = []
for item in ft:
    try:
        (timee, cwnd, nxt, una) = item
    except Exception:
        continue
    timee = int(timee)
    cwnd = int(cwnd)
    wdata.append([timee, cwnd])
tmplist = iwsurveyqueuewindow + wdata
tmplist = sorted(tmplist)
print("sss", len(tmplist))
iwsurveyqueuewindowuna = []
is_last = []
fw.writerow(["timex", "signal", "time_busy_b", "time_rx_b",
             "time_tx_b", "time_scan_b", "noise_b",
             "bytes1_b", "packets_b", "qlen_b", "backlog_b",
             "drops_b", "requeues_b", "overlimits_b", "una", 'ret', "cwnd"])
for item in tmplist:
    # print(len(item))
    try:
        (timex, signal, time_busy_b, time_rx_b,
            time_tx_b, time_scan_b, noise_b, bytes1_b,
         packets_b, qlen_b, backlog_b, drops_b,
         requeues_b, overlimits_b, una, ret) = item
        is_last = [timex, signal, time_busy_b,
                   time_rx_b, time_tx_b, time_scan_b, noise_b,
                   bytes1_b, packets_b, qlen_b,
                   backlog_b, drops_b, requeues_b, overlimits_b, una, ret]
    except Exception:
        (timee, cwnd) = item
        tmp = [cwnd]
        if len(is_last) > 0:
            # iwsurveyqueuewindow.append(is_last + tmp)
            fw.writerow(is_last + tmp)
            is_last = []
# del iwsurveyqueue
# gc.collect()
# print(iwsurveyqueuewindow)
# print(len(iwsurveyqueuewindow))
if ff1:
    ff1.close()
if ff2:
    ff2.close()
