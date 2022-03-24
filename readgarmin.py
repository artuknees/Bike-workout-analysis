import csv
import numpy as np
from datetime import datetime
import time
import matplotlib.pyplot as plt

def read():
    filename = 'GOTOES_FIT-CSV_2595200649388790.csv'
    file = open (filename)
    type(file)
    csvreader=csv.reader(file)
    header = next(csvreader)
    # print(header)
    rows = []
    for row in csvreader:
        rows.append(row)
    # print(rows)
    file.close()
    return rows

def carga(rows):
    a = np.zeros((len(rows),7))

    for i in range(len(rows)):

        #timestamp
        origin = time.mktime(datetime.strptime(rows[0][1], "%Y-%m-%dT%H:%M:%S").timetuple())
        if rows[i][1]!='':
            a[i,0] = time.mktime(datetime.strptime(rows[i][1], "%Y-%m-%dT%H:%M:%S").timetuple())-origin
        else:
            a[i,0] = 0

        #altitud
        if rows[i][4]!='':
            a[i,1] = rows[i][4]
        else:
            a[i,1] = 0

        #heart rate
        if rows[i][5]!='':
            a[i,2] = rows[i][5]
        else:
            a[i,2] = 0

        #cadence
        if rows[i][6]!='':
            a[i,3] = rows[i][6]
        else:
            a[i,3] = 0

        #distance
        if rows[i][7]!='':
            a[i,4] = rows[i][7]
        else:
            a[i,4] = 0

        #speed
        if rows[i][8]!='':
            a[i,5] = rows[i][8]
        else:
            a[i,5] = 0     

        #power
        if rows[i][9]=='':
            a[i,6] = 0 
        if int(rows[i][9])==65535:
            a[i,6] = 0 
        else:
            a[i,6] = rows[i][9]

    return a

def plotear(a):

    plt.figure(1)

    plt.plot(a[:,0]/60,a[:,6],)
    plt.grid()
    # plt.suptitle('Tiempos de llenado por operación', fontsize=18)
    plt.title('Potencia vs Tiempo')
    plt.ylabel('Potencia [watts]')
    plt.xlabel('Tiempo [min]')
    plt.show()





datos=carga(read())
plotear(datos)