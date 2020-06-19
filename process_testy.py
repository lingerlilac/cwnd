# from keras.callbacks import ModelCheckpoint
# from keras.models import Sequential
# from keras.layers import Dense, Activation, Flatten
from matplotlib import pyplot as plt
# import seaborn as sb
# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)


def get_data():
    # get test data
    train_data_path = 'Submission(XGB).csv.csv'
    train = pd.read_csv(train_data_path)
    # train['SalePrice'] = math.pow(train['SalePrice'], 1.0 / 1.38431) * 20

    # test['SalePrice'] = (test['SalePrice'] / 20)**1.38431

    test_data_path = 'test_y.csv'
    test = pd.read_csv(test_data_path)
    # print(test)
    # test['SalePrice'] = (test['SalePrice'] / 20)**1.38431
    return test, train

origin = []
test, train = get_data()
x = 1.0 / 1.38431
for i in train['SalePrice']:
    tmp = math.pow(i, x) * 20
    origin.append(tmp)
plt.plot(test, label='predict')
plt.plot(origin, label='origin')
plt.legend()
plt.show()
