import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.font_manager
import glob
# Import models
from pyod.models.abod import ABOD
from pyod.models.cblof import CBLOF
from pyod.models.feature_bagging import FeatureBagging
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.knn import KNN
from pyod.models.lof import LOF
from sklearn.preprocessing import MinMaxScaler

def IFo(df,C1):
    isolation_forest = IForest(n_estimators=100)
    isolation_forest.fit(df[C1].values.reshape(-1, 1))
    xx = np.linspace(df[C1].min(), df[C1].max(), len(df)).reshape(-1,1)
    anomaly_score = isolation_forest.decision_function(xx)
    outlier = isolation_forest.predict(xx)
    plt.figure(figsize=(10,4))
    plt.plot(xx, anomaly_score, label='anomaly score')
    plt.fill_between(xx.T[0], np.min(anomaly_score), np.max(anomaly_score),
                 where=outlier==1, color='r',
                 alpha=.4, label='outlier region')
    plt.legend()
    plt.ylabel('anomaly score')
    plt.xlabel(C1)
    plt.show();

def CAnomaly(num,C1,C2,Filename,graphing=True): #Referenced from https://www.analyticsvidhya.com/blog/2019/02/outlier-detection-python-pyod/?#
    df = dataframes[int(num)]
    df = df.dropna()
    scaler = MinMaxScaler(feature_range=(0, 1))
    df[[C1,C2]] = scaler.fit_transform(df[[C1,C2]])
    df[[C1,C2]].head()

    X1 = df[C1].values.reshape(-1,1)
    X2 = df[C2].values.reshape(-1,1)

    X = np.concatenate((X1,X2),axis=1)

    random_state = np.random.RandomState(42)
    outliers_fraction = 0.05
    # Define seven outlier detection tools to be compared
    classifiers = {
        #'Angle-based Outlier Detector (ABOD)': ABOD(contamination=outliers_fraction),
        #'Cluster-based Local Outlier Factor (CBLOF)':CBLOF(contamination=outliers_fraction,check_estimator=False, random_state=random_state),
        #'Feature Bagging':FeatureBagging(LOF(n_neighbors=35),contamination=outliers_fraction,check_estimator=False,random_state=random_state),
        #'Histogram-base Outlier Detection (HBOS)': HBOS(contamination=outliers_fraction),
        'Isolation Forest': IForest(contamination=outliers_fraction,random_state=random_state)#,
        #'K Nearest Neighbors (KNN)': KNN(contamination=outliers_fraction),
        #'Average KNN': KNN(method='mean',contamination=outliers_fraction)
        }

    xx , yy = np.meshgrid(np.linspace(0,1 , 200), np.linspace(0, 1, 200))

    for i, (clf_name, clf) in enumerate(classifiers.items()):
        clf.fit(X)
        # predict raw anomaly score
        scores_pred = clf.decision_function(X) * -1

        # prediction of a datapoint category outlier or inlier
        y_pred = clf.predict(X)
        n_inliers = len(y_pred) - np.count_nonzero(y_pred)
        n_outliers = np.count_nonzero(y_pred == 1)
        print('For Room '+str(num+1)+' OUTLIERS : ',n_outliers,'INLIERS : ',n_inliers, clf_name)


        # copy of dataframe
        dfx = df
        dfx['outlier'] = y_pred.tolist()
        dfx.to_csv(Filename,index=False)

        if graphing == True:
            plt.figure(figsize=(10, 10))
            # IX1 - inlier feature 1,  IX2 - inlier feature 2
            IX1 =  np.array(dfx[C1][dfx['outlier'] == 0]).reshape(-1,1)
            IX2 =  np.array(dfx[C2][dfx['outlier'] == 0]).reshape(-1,1)

            # OX1 - outlier feature 1, OX2 - outlier feature 2
            OX1 =  dfx[C1][dfx['outlier'] == 1].values.reshape(-1,1)
            OX2 =  dfx[C2][dfx['outlier'] == 1].values.reshape(-1,1)


            # threshold value to consider a datapoint inlier or outlier
            threshold = stats.scoreatpercentile(scores_pred,100 * outliers_fraction)

            # decision function calculates the raw anomaly score for every point
            Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()]) * -1
            Z = Z.reshape(xx.shape)

            # fill blue map colormap from minimum anomaly score to threshold value
            plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), threshold, 7),cmap=plt.cm.Blues_r)

            # draw red contour line where anomaly score is equal to thresold
            a = plt.contour(xx, yy, Z, levels=[threshold],linewidths=2, colors='red')

            # fill orange contour lines where range of anomaly score is from threshold to maximum anomaly score
            plt.contourf(xx, yy, Z, levels=[threshold, Z.max()],colors='orange')

            b = plt.scatter(IX1,IX2, c='white',s=20, edgecolor='k')

            c = plt.scatter(OX1,OX2, c='black',s=20, edgecolor='k')

            plt.axis('tight')

            # loc=2 is used for the top left corner
            plt.legend(
                [a.collections[0], b,c],
                ['learned decision function', 'inliers','outliers'],
                prop=matplotlib.font_manager.FontProperties(size=20),
                loc=2)

            plt.xlim((0, 1))
            plt.ylim((0, 1))
            plt.title(clf_name)
            plt.show()
