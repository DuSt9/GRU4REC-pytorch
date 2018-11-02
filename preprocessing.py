# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 16:20:12 2015

@author: Balázs Hidasi
"""

import numpy as np
import pandas as pd
import datetime as dt

PATH_TO_ORIGINAL_DATA = 'data/raw_data/'
PATH_TO_PROCESSED_DATA = 'data/test_data/'

data = pd.read_csv(PATH_TO_ORIGINAL_DATA + 'yoochoose-clicks-small.dat', sep=',', header=None, usecols=[0, 1, 2], dtype={0:np.int32, 1:str, 2:np.int64})
data.columns = ['SessionId', 'TimeStr', 'ItemId']
data['Time'] = data.TimeStr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()) #This is not UTC. It does not really matter.
del(data['TimeStr'])

session_lengths = data.groupby('SessionId').size()
data = data[np.in1d(data.SessionId, session_lengths[session_lengths>1].index)]
item_supports = data.groupby('ItemId').size()
data = data[np.in1d(data.ItemId, item_supports[item_supports>=5].index)]
session_lengths = data.groupby('SessionId').size()
data = data[np.in1d(data.SessionId, session_lengths[session_lengths>=2].index)]

print(data)

tmax = data.Time.max()
tmin = data.Time.min()
print("tmax = {}".format(tmax))
print(type(tmax))
print("tmin = {}".format(tmin))
print(type(tmin))
session_max_times = data.groupby('SessionId').Time.max()
print(session_max_times)

print(session_max_times.sort_values())
print(session_max_times.sort_values().data[0])


# ----------------------------------------------'

# print("session_max_times")
# print(session_max_times)
# print(type(session_max_times))
# print(session_max_times.size)
# print(session_max_times.index[-1]) # get index in pandas.Series
#
# Size = session_max_times.size
# print("Type of size: {}".format(type(Size)))
# tt = Size // 10
# print("tt = {}".format(tt))
# time = session_max_times.index[-tt]
# print("time = {}".format(time))
# print(session_max_times.sort_values())
# print(type(session_max_times.sort_values()))
# print(session_max_times.sort_values())

# Index cua cac session lam train
session_train = session_max_times[session_max_times < tmax-86400].index


# sub_train = session_max_times[session_max_times >= time].index # 10% of training data
# sub_train = data[np.in1d(data.SessionId, sub_train)]
# print("sub_train")
# print(sub_train)


# sus_train = session_max_times[session_max_times >= ]
print(session_train)
# Index cua cac session lam test
session_test = session_max_times[session_max_times >= tmax-86400].index
train = data[np.in1d(data.SessionId, session_train)]
test = data[np.in1d(data.SessionId, session_test)]


tmax = train.Time.max()
tmin = train.Time.min()
print("tmax = {}".format(tmax))
print(type(tmax))
print("tmin = {}".format(tmin))
print(type(tmin))

session_max_times = train.groupby('SessionId').Time.max()
Size = session_max_times.size
print("Size = {}".format(Size))
tt = Size // 10
print("print index train")
print(type(session_max_times.sort_values()))
print(session_max_times.sort_values())

time = session_max_times.sort_values().data[-tt]
print("time = {}".format(time))
print(type(time))
print("time = {}".format(time))
session_add = session_max_times[session_max_times >= time].index
sub_train = train[np.in1d(train.SessionId, session_add)]

session_min = sub_train.SessionId.min()
print("session_min = {}".format(session_min))

print(sub_train)
# print("test item")
# print(test.ItemId)
#
# print("train item")
# print(train.ItemId)




# =================================================================================
test = test[np.in1d(test.ItemId, train.ItemId)]
tslength = test.groupby('SessionId').size()
test = test[np.in1d(test.SessionId, tslength[tslength>=2].index)]
print('Full train set\n\tEvents: {}\n\tSessions: {}\n\tItems: {}'.format(len(train), train.SessionId.nunique(), train.ItemId.nunique()))
train.to_csv(PATH_TO_PROCESSED_DATA + 'rsc15_train_full.txt', sep='\t', header=False, index=False)
print('Test set\n\tEvents: {}\n\tSessions: {}\n\tItems: {}'.format(len(test), test.SessionId.nunique(), test.ItemId.nunique()))
test.to_csv(PATH_TO_PROCESSED_DATA + 'rsc15_test.txt', sep='\t', header=False, index=False)
print('Sub set\n\tEvents: {}\n\tSessions: {}\n\tItems: {}'.format(len(sub_train), sub_train.SessionId.nunique(), sub_train.ItemId.nunique()))

tmax = train.Time.max()
session_max_times = train.groupby('SessionId').Time.max()
session_train = session_max_times[session_max_times < tmax-86400].index
session_valid = session_max_times[session_max_times >= tmax-86400].index
train_tr = train[np.in1d(train.SessionId, session_train)]
valid = train[np.in1d(train.SessionId, session_valid)]
valid = valid[np.in1d(valid.ItemId, train_tr.ItemId)]
tslength = valid.groupby('SessionId').size()
valid = valid[np.in1d(valid.SessionId, tslength[tslength>=2].index)]
print('Train set\n\tEvents: {}\n\tSessions: {}\n\tItems: {}'.format(len(train_tr), train_tr.SessionId.nunique(), train_tr.ItemId.nunique()))
train_tr.to_csv(PATH_TO_PROCESSED_DATA + 'rsc15_train_tr.txt', sep='\t', header=False, index=False)
print('Validation set\n\tEvents: {}\n\tSessions: {}\n\tItems: {}'.format(len(valid), valid.SessionId.nunique(), valid.ItemId.nunique()))
valid.to_csv(PATH_TO_PROCESSED_DATA + 'rsc15_train_valid.txt', sep='\t', header=False, index=False)
