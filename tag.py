
def tag_anomaly(df):
    ADP = df['ADP']
    DPAS = df['DPAS']
    DATHWVC = df['DATHWVC']
    a = []
    b = []
    c = []
    for i in range(len(ADP)):
        if ADP[i] >= 0.25:
            ADP[i] = 1
        else:
            ADP[i] = 0
            a.append(i)
    for i in range(len(DPAS)):
        if DPAS[i] >= 0.5:
            DPAS[i] = 1
        else:
            DPAS[i] = 0
            b.append(i)
    for i in range(len(DATHWVC)):
        if DATHWVC[i] < 1 and DATHWVC[i] > 0.5:
            DATHWVC[i] = 1
        else:
            DATHWVC[i] = 0
            c.append(i)
    print('ADP Anomalies exist in file index:')
    print(a)
    print('DPAS Anomalies exist in file index:')
    print(b)
    print('DATHWVC Anomalies exist in file index:')
    print(b)
    return df

def tag_constants(df):
    pass
