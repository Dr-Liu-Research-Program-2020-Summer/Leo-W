import numpy as np
import matplotlib.pyplot as plt

def normalize(list1):
    minx = min(list1)
    base = max(list1)-min(list1)
    normalized = [(x - minx)/base for x in list1]
    return normalized

def FFT_with_graphes(list):
    n = len(list)
    nl = normalize(list)
    FK1 =  np.fft.fft(nl)/n
    dx = 5 #min
    NF1 = np.fft.fftfreq(n,dx)
    value = np.arange(n)
    FK = np.fft.fftshift(FK1)
    NF = np.fft.fftshift(NF1)
    f, ax = plt.subplots(2,1)
    plt.subplots_adjust(hspace=1)
    ax[0].plot(value/   n, abs(FK1))
    ax[1].plot(NF,np.absolute(FK)*2)
    plt.show()
