import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def normalize(list1):
    minx = min(list1)
    base = max(list1)-min(list1)
    normalize = [(x - minx)/base for x in list1]
    return normalize

def check_outliers(X):
    l = np.where(abs(X - np.mean(X)) >= 4 * np.std(X))
    return l[0].tolist()

def remove_outliers(y,X):
    ind1 = check_outliers(X)
    ind2 = check_outliers(y)
    ind = np.union1d(ind1, ind2).astype(int).tolist()
    X = np.delete(X,ind)
    y = np.delete(y,ind)
    return y,X

def check_constant(sequence):
    if (np.count_nonzero(np.diff(sequence)==0)/len(sequence)) >= 0.99:  # unchange at more than 99% of the time
        sequence = np.append(sequence,'constant')
    return sequence


def tlcc_pearson(y, X, lag_limit=20):  # time-step is 90s due to rules of signal collection, upper bound of moving lag term is 30mins/90s=20
    clst=[]
    y,X = remove_outliers(y,X)
    y = check_constant(y)
    X = check_constant(X)
    for i in range(lag_limit): # 1 time-steps per movement
        if ((y[-1]=='constant')|(X[-1]=='constant')):    # return 99 if sequence is
            j=0
            clst.append(2)
            break
        x_lag = X[0:len(X)-1*i]
        y_lag = y[i:,]
        corr = round(stats.pearsonr(y_lag,x_lag)[0],3)
        clst.append(corr)
    #print(clst)
    j = np.argmax(np.absolute(clst))  # first occurance
    return j, clst[j]

def tlcc_spearman(y, X, lag_limit=20):  # time-step is 90s due to rules of signal collection, upper bound of moving lag term is 30mins/90s=20
    clst=[]
    y,X = remove_outliers(y,X)
    y = check_constant(y)
    X = check_constant(X)
    for i in range(lag_limit): # 1 time-steps per movement
        if ((y[-1]=='constant')|(X[-1]=='constant')):    # return 99 if sequence is
            j=0
            clst.append(2)
            break
        x_lag = X[0:len(X)-1*i]
        y_lag = y[i:,]
        corr = round(stats.spearmanr(y_lag,x_lag)[0],3)
        #corr = round(stats.pearsonr(np.nan_to_num((y_lag).astype(float)),np.nan_to_num((x_lag).astype(float)))[0],3)
        clst.append(corr)
    #print(clst)
    j = np.argmax(np.absolute(clst))  # first occurance
    return j, clst[j]
