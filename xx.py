from sklearn.ensemble import VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import ExtraTreesRegressor
# from sklearn.ensemble import StackingRegressor
from sklearn import datasets
import csv
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LassoCV
from sklearn.linear_model import RidgeCV
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
"""
=================================================
Plot individual and voting regression predictions
=================================================

.. currentmodule:: sklearn

Plot individual and averaged regression predictions for Boston dataset.

First, three exemplary regressors are initialized
(:class:`~ensemble.GradientBoostingRegressor`,
:class:`~ensemble.RandomForestRegressor`, and
:class:`~linear_model.LinearRegression`) and used to initialize a
:class:`~ensemble.VotingRegressor`.

The red starred dots are the averaged predictions.

"""
print(__doc__)


try:
    ff1 = open('xxx.csv', 'r')
    fr1 = csv.reader(ff1)
except Exception:
    print('dataset.csv openfailed')
    exit()
X = []
y = []
for item in fr1:
    pass
    break
for item in fr1:
    if (len(item) == 0):
        continue
    # print(item)
    (window, una, packets_b) = [float(item[i]) for i in range(0, len(item))]
    X.append([una, packets_b])
    y.append(window)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3)
estimators = [
    ('Random Forest', RandomForestRegressor(random_state=42)),
    ('Lasso', LassoCV()),
    ('Gradient Boosting', GradientBoostingRegressor(random_state=0))
]
# reg7 = StackingRegressor(
#     estimators=estimators, final_estimator=RidgeCV()
# )
# Loading some example data
# X, y = datasets.load_boston(return_X_y=True)
# print(X)
# print(y)
# exit()
# Training classifiers
reg1 = GradientBoostingRegressor()
# reg2 = RandomForestRegressor()
# reg3 = LinearRegression()
# ereg = VotingRegressor([('gb', reg1), ('rf', reg2), ('lr', reg3)])
# reg4 = AdaBoostRegressor()
# reg5 = BaggingRegressor()
# reg6 = ExtraTreesRegressor()
reg8 = XGBRegressor()

reg8.fit(X_train, y_train)
reg1.fit(X_train, y_train)
# reg2.fit(X_train, y_train)
# reg3.fit(X_train, y_train)
# ereg.fit(X_train, y_train)
# reg4.fit(X_train, y_train)
# reg5.fit(X_train, y_train)
# reg6.fit(X_train, y_train)
# reg7.fit(X_train, y_train)
print("GradientBoostingRegressor:", reg1.score(X_test, y_test))
# print("RandomForestRegressor:", reg2.score(X_test, y_test))
# print("LinearRegression:", reg3.score(X_test, y_test))
# print("VotingRegressor:", ereg.score(X_test, y_test))
# print("AdaBoostRegressor:", reg4.score(X_test, y_test))
# print("BaggingRegressor:", reg5.score(X_test, y_test))
# print("ExtraTreesRegressor:", reg6.score(X_test, y_test))
# print("StackingRegressor:", reg7.score(X_test, y_test))
print("XGBRegressor:", reg8.score(X_test, y_test))

XGBpredictions = reg8.predict(X_test)
MAE = mean_absolute_error(y_test, XGBpredictions)
print('XGBoost validation MAE = ', MAE)
xx = []
# try:
#     file = open('regression.csv', 'w', newline='')
#     file_w = csv.writer(file)
# except Exception:
#     print('regression.csv open faild')
#     exit()
# names = ['test', 'prediction']
# file_w.writerow(names)
# for i in range(0, len(y_test)):
#     tmp = [y_test[i], XGBpredictions[i]]
#     file_w.writerow(tmp)
# if file:
#     file.close()
# print("ok")
# exit()
for i in range(0, len(y_test)):
    xx.append(i)
plt.plot(xx, y_test)
plt.plot(xx, XGBpredictions)
plt.savefig("regression.pdf")
plt.show()
