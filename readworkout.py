import csv
from datetime import datetime
import time
import matplotlib.pyplot as plt


class Workout:
    def __init__(self):
        self.timestamp = []
        self.altitude = []
        self.heart_rate = []
        self.cadence = []
        self.speed = []
        self.power = []
        self.power_3s = []
        self.power_10s = []

    def load_data(self):
        rows = []
        filename = 'GOTOES_FIT-CSV_5156920312294904.csv'
        file = open (filename)
        type(file)
        csvreader=csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
        file.close()
       
        for i in range(len(rows)):
            #timestamp
            origin = time.mktime(datetime.strptime(rows[0][1], "%Y-%m-%dT%H:%M:%S").timetuple())
            if rows[i][1]!='':
                self.timestamp.append(time.mktime(datetime.strptime(rows[i][1], "%Y-%m-%dT%H:%M:%S").timetuple())-origin)
            else:
                self.timestamp.append(0)

            #altitud
            if rows[i][4]!='':
                self.altitude.append(float(rows[i][4]))
            else:
                self.altitude.append(0)

            #heart rate
            if rows[i][5]!='':
                self.heart_rate.append(float(rows[i][5]))
            else:
                self.heart_rate.append(self.heart_rate[-1])


            # #cadence
            if rows[i][6]!='':
                self.cadence.append(float(rows[i][6]))
            else:
                self.cadence.append(0)

            # #distance
            # if rows[i][7]!='':
            #     a[i,4] = rows[i][7]
            # else:
            #     a[i,4] = 0

            #speed
            if rows[i][8]!='':
                self.speed.append(float(rows[i][8]))
            else:
                self.speed.append(0)    

            #power
            if rows[i][9]=='':
                self.power.append(0)
            elif int(rows[i][9])==65535:
                self.power.append(0)
            else:
                self.power.append(float(rows[i][9]))

    def analyze(self):
        muestras = 3
        limit = list(range(0,muestras-1)) # defino la cantidad de tomas. 1 menos que la cantidad de segundos.
        for i in range(len(self.timestamp)):
            # if i == 0 or i == 1:
            if i in limit:
                self.power_3s.append(0)
            else:
                power_3s_adjunt = sum(self.power[i-(muestras-1):i+1])/muestras
                self.power_3s.append(power_3s_adjunt)

        muestras_10 = 10
        limit = list(range(0,muestras_10-1)) # defino la cantidad de tomas. 1 menos que la cantidad de segundos.
        for i in range(len(self.timestamp)):
            # if i == 0 or i == 1:
            if i in limit:
                self.power_10s.append(0)
            else:
                power_10s_adjunt = sum(self.power[i-(muestras_10-1):i+1])/muestras_10
                self.power_10s.append(power_10s_adjunt)


        seconds = [1,2,5,10,15,20,30,45,60,90,120,150,180,300,600,1200,1800,3600,7200]
        secondsstr = [str(el) for el in seconds]
        power_avg = []
        for n in seconds:
            limite = list(range(0,n-1)) # defino la cantidad de tomas. 1 menos que la cantidad de segundos.
            max_power_avg = 0
            for i in range(len(self.timestamp)):
                if i in limite:
                    pass
                else:
                    power_compare = sum(self.power[i-(n-1):i+1])/n
                    if power_compare > max_power_avg:
                        max_power_avg = power_compare

            power_avg.append(round(max_power_avg))
        print('Picos de potencia para {} segundos'.format(seconds))
        print('{} watts'.format(power_avg))

        fig, ax = plt.subplots(3)
        ax[0].plot([el/60 for el in self.timestamp],self.power)
        ax[0].grid()
        ax[0].set_title('Power - Inst. vs. 3 sec. vs. 10 sec.')
        ax[1].plot([el/60 for el in self.timestamp],self.power_3s)
        ax[1].grid()
        ax[2].plot([el/60 for el in self.timestamp],self.power_10s)
        ax[2].grid()
        ax[2].set_xlabel('Time [min.]')
        ax[0].set_ylabel('Power [watts]')
        ax[1].set_ylabel('Power [watts]')
        ax[2].set_ylabel('Power [watts]')

        plt.figure(0)
        plt.plot(secondsstr,power_avg)
        plt.grid()
        plt.title('Workout peaks')
        plt.xlabel('Time [sec.]')
        plt.ylabel('Power [watts]')

        fig, ax1 = plt.subplots()
        ax1.plot([el/60 for el in self.timestamp],self.heart_rate,'r')
        ax1.set_xlabel('Time [min.]')
        ax1.set_ylabel('Heart Rate [bpm]', color = 'red')
        ax1.grid()
        ax1.set_title('Heart Rate vs. Power')
        ax2 = ax1.twinx()
        ax2.plot([el/60 for el in self.timestamp],self.power_3s)
        ax2.set_ylabel('Power [watts]', color = 'blue')

        plt.show()

instance = Workout()
instance.load_data()
instance.analyze()
