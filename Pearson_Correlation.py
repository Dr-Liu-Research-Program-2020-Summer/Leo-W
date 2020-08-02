import pandas as pd
from scipy.stats import pearsonr
import glob

def Pearson_Dataframe(Filename):
    filenames = glob.glob('./Data/*.csv')
    dataframes = [pd.read_csv(f) for f in filenames]
    df = pd.DataFrame(columns=['ADP','ADAT','AZT','AAS','AHWVC','DPDAT','DPZT','DPAS','DPHWVC','DATZT','DATAS','DATHWVC','ZTAS','ZTHWVC','ASHWVC'])
    for i in range(len(dataframes)):
        room = dataframes[i]
        room = room.dropna()
        ADP,p1 = pearsonr(room['AirFlow'],room['Damper Position'])
        ADAT,p2 = pearsonr(room['AirFlow'],room['Discharge Air Temperature'])
        AZT,p3 = pearsonr(room['AirFlow'],room['Zone Temperature'])
        AAS,p4 = pearsonr(room['AirFlow'],room['Airflow Setpoint'])
        AHWVC,p5 = pearsonr(room['AirFlow'],room['Hot Water Valve Command '])
        DPDAT,p6 = pearsonr(room['Damper Position'],room['Discharge Air Temperature'])
        DPZT,p7 = pearsonr(room['Damper Position'],room['Zone Temperature'])
        DPAS,p8 = pearsonr(room['Damper Position'],room['Airflow Setpoint'])
        DPHWVC,p9 = pearsonr(room['Damper Position'],room['Hot Water Valve Command '])
        DATZT,p10 = pearsonr(room['Discharge Air Temperature'],room['Zone Temperature'])
        DATAS,p11 = pearsonr(room['Discharge Air Temperature'],room['Airflow Setpoint'])
        DATHWVC,p12 = pearsonr(room['Discharge Air Temperature'],room['Hot Water Valve Command '])
        ZTAS,p13 = pearsonr(room['Zone Temperature'],room['Airflow Setpoint'])
        ZTHWVC,p14 = pearsonr(room['Zone Temperature'],room['Hot Water Valve Command '])
        ASHWVC,p15 = pearsonr(room['Airflow Setpoint'],room['Hot Water Valve Command '])
        data = {'ADP':ADP,'ADAT':ADAT,'AZT':AZT,'AAS':AAS,'AHWVC':AHWVC,'DPDAT':DPDAT,'DPZT':DPZT,'DPAS':DPAS,'DPHWVC':DPHWVC,'DATZT':DATZT,'DATAS':DATAS,'DATHWVC':DATHWVC,'ZTAS':ZTAS,'ZTHWVC':ZTHWVC,'ASHWVC':ASHWVC}
        df = df.append(data,ignore_index=True,sort=False)
        #print(data)
    #print(df)
    df.fillna(0, inplace=True)
    df.to_csv(Filename)
