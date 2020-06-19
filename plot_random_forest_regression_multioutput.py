"""
============================================================
Comparing random forests and the multi-output meta estimator
============================================================

An example to compare multi-output regression with random forest and
the :ref:`multioutput.MultiOutputRegressor <multiclass>` meta-estimator.

This example illustrates the use of the
:ref:`multioutput.MultiOutputRegressor <multiclass>` meta-estimator
to perform multi-output regression. A random forest regressor is used,
which supports multi-output regression natively, so the results can be
compared.

The random forest regressor will only ever predict values within the
range of observations or closer to zero for each of the targets. As a
result the predictions are biased towards the centre of the circle.

Using a single underlying feature the model learns both the
x and y coordinate as output.

"""
print(__doc__)

# Author: Tim Head <betatim@gmail.com>
#
# License: BSD 3 clause

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
import csv

# Create a random dataset
try:
    ff1 = open('dataset.csv', 'r')
    fr1 = csv.reader(ff1)
except Exception:
    print('dataset.csv openfailed')
    exit()
X = []
y = []
for item in fr1:
    break
for item in fr1:
    # print(len(item))
    (signal, time_busy_b, time_rx_b, time_tx_b, time_scan_b,
     noise_b, bytes1_b, packets_b, qlen_b, backlog_b, drops_b,
     requeues_b, overlimits_b, una, window) = [float(item[i]) for i in range(1, len(item) - 1)]
    X.append([una, signal, time_busy_b, time_rx_b, time_tx_b, time_scan_b,
     noise_b, bytes1_b, packets_b, qlen_b, backlog_b, drops_b,
     requeues_b, overlimits_b])
    y.append(window)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3)

max_depth = 30
regr_multirf = MultiOutputRegressor(RandomForestRegressor(n_estimators=100,
                                                          max_depth=max_depth,
                                                          random_state=0))
regr_multirf.fit(X_train, y_train)

regr_rf = RandomForestRegressor(n_estimators=100, max_depth=max_depth,
                                random_state=2)
regr_rf.fit(X_train, y_train)

# Predict on new data
y_multirf = regr_multirf.predict(X_test)
y_rf = regr_rf.predict(X_test)

# Plot the results
plt.figure()
s = 50
a = 0.4
plt.scatter(y_test[:, 0], y_test[:, 1], edgecolor='k',
            c="navy", s=s, marker="s", alpha=a, label="Data")
plt.scatter(y_multirf[:, 0], y_multirf[:, 1], edgecolor='k',
            c="cornflowerblue", s=s, alpha=a,
            label="Multi RF score=%.2f" % regr_multirf.score(X_test, y_test))
plt.scatter(y_rf[:, 0], y_rf[:, 1], edgecolor='k',
            c="c", s=s, marker="^", alpha=a,
            label="RF score=%.2f" % regr_rf.score(X_test, y_test))
plt.xlim([-6, 6])
plt.ylim([-6, 6])
plt.xlabel("target 1")
plt.ylabel("target 2")
plt.title("Comparing random forests and the multi-output meta estimator")
plt.legend()
plt.show()
