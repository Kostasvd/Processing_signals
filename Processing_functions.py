import numpy as np
import scipy.signal
import pandas
from matplotlib import pyplot as plt
from detect_peaks import detect_peaks
#import data from .csv
colnames = [ 'voltage']
data = pandas.read_csv('K:/Location/file.csv', names=colnames)
voltage = data.voltage.tolist()
plt.plot(voltage)
plt.savefig('plot1')
plt.show()
    #calculate time and voltage scale
t=1/100000
s=(3.000/8191)*(20/1.800)
#invert voltage, then detect peaks for frequency and period calculation
minus=[-1]*len(voltage)
m=[0]*len(voltage)
for i in range(len(voltage)):
    voltage1=minus[i]*voltage[i]
    m[i]=voltage1
plt.plot(m)
plt.show()
indexes = detect_peaks(m, mph=-1000, mpd=500)
print(indexes)
r=0
#Period and frequency
for i in range(len(indexes)-1):
    r=abs(indexes[i]-indexes[i+1])+r
r=r/(len(indexes)-1)*t
n=1/r
print('r =',r)
print('n =',n)
#find area for calculating parameters
voltage=voltage[indexes[0]-1000:indexes[0]+1000]
plt.plot(voltage)
plt.show()
#filter "voltage" with butterworth filter
b, a = scipy.signal.butter(2, 0.07, btype='highpass', analog=False)
voltage_filt=scipy.signal.filtfilt(b,a,voltage)
plt.plot(voltage_filt)
plt.show()
#adaptive mph calculation for each case
k=50/585.174 
h=k*max(voltage_filt)
print(h)
#detect peaks
indexes = detect_peaks(voltage_filt, mph=h, mpd=20)
#indexes = detect_peaks(m, mph=-4000, mpd=50)
print(indexes)
#calculating distance
T=(indexes[len(indexes)-1]-indexes[0])*t
ti=(indexes[1]-indexes[0])*t if (indexes[1]-indexes[0])<(indexes[2]-indexes[1]) else (indexes[2]-indexes[1])*t 
#array of indexes
arg=[0]*len(voltage)
for i in range(len(voltage)):
    arg[i]=i
#calculating constant level(20V)
b1=arg[0:indexes[0]]
b2=arg[indexes[len(indexes)-1]+1:len(arg)]
s1=0
s2=0
for i in b1:
    s1=voltage[i]+s1
for i in b2:
    s2=voltage[i]+s2    
const_level=(s1+s2)*s/(indexes[0]+len(arg)-indexes[len(indexes)-1])
#calculating big amplitude
b3=arg[indexes[0]:indexes[1]]
b4=arg[indexes[1]:indexes[2]]
b5=arg[indexes[2]:indexes[len(indexes)-1]]

s3=0
s4=0
if (indexes[1]-indexes[0])<(indexes[2]-indexes[1]):
    for i in b4:
        s3=voltage[i]+s3
    A=s3*s/(indexes[2]-indexes[1])
elif (indexes[len(indexes)-1]-indexes[2])<(indexes[2]-indexes[1]):
    for i in b3:
        s4=voltage[i]+s4
    A=s4*s/(indexes[1]-indexes[0])
else:
    for i in b3:
        s3=voltage[i]+s3
    for i in b5:
        s4=voltage[i]+s4    
    A=(s3+s4)*s/(indexes[1]-indexes[0]+indexes[len(indexes)-1]-indexes[2])
#calculating small amplitude
s5=0
if (indexes[1]-indexes[0])<(indexes[2]-indexes[1]):
    for j in b3:
        s5=voltage[j]+s5
    a=s5*s/(indexes[1]-indexes[0])
else:
    for j in b4:
        s5=voltage[j]+s5
    a=s5*s/(indexes[2]-indexes[1])
#printing and showing everything
print('T=',T)
print('ti=',ti)
print('Constant Level =',const_level) 
print('A=',A)
print('a=',a)
