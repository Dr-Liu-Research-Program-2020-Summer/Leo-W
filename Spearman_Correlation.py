import pandas as pd
from scipy.stats import spearmanr
import glob

def Correlation_Dataframe(Filename):
    filenames = glob.glob('./Data/*.csv')
    dataframes = [pd.read_csv(f) for f in filenames]
    df = pd.DataFrame(columns=['ADP','ADAT','AZT','AAS','AHWVC','DPDAT','DPZT','DPAS','DPHWVC','DATZT','DATAS','DATHWVC','ZTAS','ZTHWVC','ASHWVC'])
    for i in range(len(dataframes)):
        room = dataframes[i]
        room = room.dropna()
        ADP,p1 = spearmanr(room['AirFlow'],room['Damper Position'])
        ADAT,p2 = spearmanr(room['AirFlow'],room['Discharge Air Temperature'])
        AZT,p3 = spearmanr(room['AirFlow'],room['Zone Temperature'])
        AAS,p4 = spearmanr(room['AirFlow'],room['Airflow Setpoint'])
        AHWVC,p5 = spearmanr(room['AirFlow'],room['Hot Water Valve Command '])
        DPDAT,p6 = spearmanr(room['Damper Position'],room['Discharge Air Temperature'])
        DPZT,p7 = spearmanr(room['Damper Position'],room['Zone Temperature'])
        DPAS,p8 = spearmanr(room['Damper Position'],room['Airflow Setpoint'])
        DPHWVC,p9 = spearmanr(room['Damper Position'],room['Hot Water Valve Command '])
        DATZT,p10 = spearmanr(room['Discharge Air Temperature'],room['Zone Temperature'])
        DATAS,p11 = spearmanr(room['Discharge Air Temperature'],room['Airflow Setpoint'])
        DATHWVC,p12 = spearmanr(room['Discharge Air Temperature'],room['Hot Water Valve Command '])
        ZTAS,p13 = spearmanr(room['Zone Temperature'],room['Airflow Setpoint'])
        ZTHWVC,p14 = spearmanr(room['Zone Temperature'],room['Hot Water Valve Command '])
        ASHWVC,p15 = spearmanr(room['Airflow Setpoint'],room['Hot Water Valve Command '])
        data = {'ADP':ADP,'ADAT':ADAT,'AZT':AZT,'AAS':AAS,'AHWVC':AHWVC,'DPDAT':DPDAT,'DPZT':DPZT,'DPAS':DPAS,'DPHWVC':DPHWVC,'DATZT':DATZT,'DATAS':DATAS,'DATHWVC':DATHWVC,'ZTAS':ZTAS,'ZTHWVC':ZTHWVC,'ASHWVC':ASHWVC}
        df = df.append(data,ignore_index=True,sort=False)
        #print(data)
    #print(df)
    df.fillna(0, inplace=True)
    df.to_csv(Filename)
