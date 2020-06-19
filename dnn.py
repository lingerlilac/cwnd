from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from matplotlib import pyplot as plt
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)
from xgboost import XGBRegressor


def get_data():
    # get train data
    train_data_path = 'train.csv'
    train = pd.read_csv(train_data_path)

    # get test data
    test_data_path = 'test.csv'
    test = pd.read_csv(test_data_path)
    train['SalePrice'] = (train['SalePrice'])
    train['una'] = (train['una'])**0.66
    train['time_tx_b'] = (train['time_tx_b'] / 10)**2.015
    train['bytes1_b'] = (train['bytes1_b']) ** 0.745
    train['time_busy_b'] = (train['time_busy_b']) ** 9 * 100

    test['una'] = (test['una'])**0.66
    test['time_tx_b'] = (test['time_tx_b'] / 10)**2.015
    test['bytes1_b'] = (test['bytes1_b']) ** 0.745
    test['time_busy_b'] = (test['time_busy_b']) ** 9 * 100
    # train.drop(['time_rx_b', 'time_scan_b', 'packets_b', 'qlen_b', 'backlog_b',
    #             'drops_b', 'requeues_b', 'overlimits_b'], axis=1, inplace=True)
    # test.drop(['time_rx_b', 'time_scan_b', 'packets_b', 'qlen_b', 'backlog_b',
    #            'drops_b', 'requeues_b', 'overlimits_b'], axis=1, inplace=True)
    return train, test


def get_combined_data():
    # reading train data
    train, test = get_data()

    target = train.SalePrice
    train.drop(['SalePrice'], axis=1, inplace=True)

    combined = train.append(test)
    combined.reset_index(inplace=True)
    combined.drop(['index', 'Id'], inplace=True, axis=1)

    return combined, target


# Load train and test data into pandas DataFrames
train_data, test_data = get_data()

# Combine train and test data to process them together
combined, target = get_combined_data()

combined.describe()


def get_cols_with_no_nans(df, col_type):
    '''
    Arguments :
    df : The dataframe to process
    col_type :
          num : to only get numerical columns with no nans
          no_num : to only get nun-numerical columns with no nans
          all : to get any columns with no nans
    '''
    if (col_type == 'num'):
        predictors = df.select_dtypes(exclude=['object'])
    elif (col_type == 'no_num'):
        predictors = df.select_dtypes(include=['object'])
    elif (col_type == 'all'):
        predictors = df
    else:
        print('Error : choose a type (num, no_num, all)')
        return 0
    cols_with_no_nans = []
    for col in predictors.columns:
        if not df[col].isnull().any():
            cols_with_no_nans.append(col)
    return cols_with_no_nans


num_cols = get_cols_with_no_nans(combined, 'num')
cat_cols = get_cols_with_no_nans(combined, 'no_num')

print('Number of numerical columns with no nan values :', len(num_cols))
print('Number of nun-numerical columns with no nan values :', len(cat_cols))


combined = combined[num_cols + cat_cols]
combined.hist(figsize=(12, 10))
# plt.show()

train_data = train_data[num_cols + cat_cols]
train_data['Target'] = target

C_mat = train_data.corr()
fig = plt.figure(figsize=(15, 15))

sb.heatmap(C_mat, vmax=.8, square=True)
# plt.show()


def oneHotEncode(df, colNames):
    for col in colNames:
        if(df[col].dtype == np.dtype('object')):
            dummies = pd.get_dummies(df[col], prefix=col)
            df = pd.concat([df, dummies], axis=1)

            # drop the encoded column
            df.drop([col], axis=1, inplace=True)
    return df


print('There were {} columns before encoding categorical features'.format(
    combined.shape[1]))
combined = oneHotEncode(combined, cat_cols)
print('There are {} columns after encoding categorical features'.format(
    combined.shape[1]))


def split_combined():
    global combined
    train = combined[:41678]
    test = combined[41678:]

    return train, test


train, test = split_combined()
# print(train)

NN_model = Sequential()

# The Input Layer :
NN_model.add(Dense(128, kernel_initializer='normal',
                   input_dim=train.shape[1], activation='relu'))

# The Hidden Layers :
NN_model.add(Dense(256, kernel_initializer='normal', activation='relu'))
NN_model.add(Dense(256, kernel_initializer='normal', activation='relu'))
NN_model.add(Dense(256, kernel_initializer='normal', activation='relu'))

# The Output Layer :
NN_model.add(Dense(1, kernel_initializer='normal', activation='linear'))

# Compile the network :
NN_model.compile(loss='mean_absolute_error', optimizer='adam',
                 metrics=['mean_absolute_error'])
NN_model.summary()

checkpoint_name = 'Weights-{epoch:03d}.hdf5'
checkpoint = ModelCheckpoint(
    checkpoint_name, monitor='val_loss', verbose=1,
    save_best_only=True, mode='auto')
callbacks_list = [checkpoint]

NN_model.fit(train, target, epochs=500, batch_size=32,
             validation_split=0.2, callbacks=callbacks_list)

train_X, val_X, train_y, val_y = train_test_split(
    train, target, test_size=0.25, random_state=14)
model = RandomForestRegressor()
model.fit(train_X, train_y)
RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=None,
                      max_features='auto', max_leaf_nodes=None,
                      min_impurity_decrease=0.0, min_impurity_split=None,
                      min_samples_leaf=1, min_samples_split=2,
                      min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
                      oob_score=False, random_state=None,
                      verbose=0, warm_start=False)
predicted_prices = model.predict(val_X)
MAE = mean_absolute_error(val_y, predicted_prices)
print('Random forest validation MAE = ', MAE)
predicted_prices = model.predict(val_X)
MAE = mean_absolute_error(val_y, predicted_prices)
print('Random forest validation MAE = ', MAE)


def make_submission(prediction, sub_name):
    my_submission = pd.DataFrame(
        {'Id': pd.read_csv('test.csv').Id, 'SalePrice': prediction})
    my_submission.to_csv('{}.csv'.format(sub_name), index=False)
    print('A submission file has been made')


XGBModel = XGBRegressor()
XGBModel.fit(train_X, train_y, verbose=False)
XGBpredictions = XGBModel.predict(val_X)
MAE = mean_absolute_error(val_y, XGBpredictions)
print('XGBoost validation MAE = ', MAE)
print(XGBModel.score(val_X, val_y))
print(model.score(val_X, val_y))
XGBpredictions = XGBModel.predict(test)
make_submission(XGBpredictions, 'Submission(XGB).csv')
print(NN_model.score(val_X, val_y))
# Load wights file of the best model :
wights_file = checkpoint_name  # choose the best checkpoint
NN_model.load_weights(wights_file)  # load it
NN_model.compile(loss='mean_absolute_error', optimizer='adam',
                 metrics=['mean_absolute_error'])


def make_submission(prediction, sub_name):
    my_submission = pd.DataFrame(
        {'Id': pd.read_csv('test.csv').Id, 'SalePrice': prediction})
    my_submission.to_csv('{}.csv'.format(sub_name), index=False)
    print('A submission file has been made')


predictions = NN_model.predict(test)
make_submission(predictions[:, 0], 'submission(NN).csv')
