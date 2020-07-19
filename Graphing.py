import matplotlib as plt

def normalize(list1):
    minx = min(list1)
    base = max(list1)-min(list1)
    normalized = [(x - minx)/base for x in list1]
    return normalized
    
def twolistcompare(list1,list2):
    normalize(list1)
    normalize(list2)
    plt.plot(list1)
    plt.plot(list2)
    plt.xticks(rotation=90)
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Value')
