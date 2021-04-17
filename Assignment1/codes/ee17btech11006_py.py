import soundfile as sf
import numpy as np
from scipy import signal, fftpack
import matplotlib.pyplot as plt
input_s,fs = sf.read('Sound_Noise.wav') 

# Time Period
Ts=1.0/fs

# Order of the filter
order=4

# Filter cutoff frequency
#cutoff_freq =4000.0

def filtering(input_s,order,Wn):
  b, a = signal.butter(order,Wn, 'low')
  output_s = signal.filtfilt(b, a, input_s)
  return output_s
def fft(input_s, Ts):
    n = input_s.shape[0]
    a = abs(fftpack.fft(input_s)) 
    a1=[]
    for i in range(n//2):
        a1.append(a[i])
    b = fftpack.fftfreq(input_s.size, Ts)
    b1=[]
    for i in range(n//2):
        b1.append(b[i])
    return  a1,b1
m,w=fft(input_s,Ts)
f=signal.find_peaks(m,height=450)
aa=f[0]
aa1=len(aa)
cutoff_freq=w[aa[len(aa)-1]]
print('cutoff_freq is',cutoff_freq)
Wn =2*cutoff_freq/fs
order=4
k=5 
## applying the filter for  multiple times
for i in range(k):
  if i==0:
    ff=filtering(input_s,order,Wn)
  if i!=0:
    ff=filtering(ff,order,Wn)
# Plotting the frequency response Original
plot1=plt.figure(1)    
a2,b2=fft(input_s,Ts)
plt.plot(b2,a2)
plt.xlim([0,5000])
plt.title("origianl")
plt.savefig('ee17btech11006_Original.eps')
plt.savefig('ee17btech11006_Original.png')
# Plotting the frequency response Filtered
plot1=plt.figure(2)
a1,b1=fft(ff,Ts)
plt.plot(b1,a1)
plt.xlim([0,5000])
plt.title("filtered")
plt.savefig('ee17btech11006_filtered.eps')
plt.savefig('ee17btech11006_filtered.png')
sf.write('optimized.wav', ff, fs) 
np.savetxt("Optimizied.dat",ff)

o1 = 0
o2 = 0
opt1 = 0
opt2 = 0

for i in range(len(w)):
    if w[i]<cutoff_freq:
        o1 += a2[i]
        opt1 += a1[i]
    if w[i]>=cutoff_freq:
        o2 += a2[i]
        opt2 += a1[i] 

print("Integral from 0 to cutoff of original signal:  ",round(o1,3))
print("Integral from 0 to cutoff of filtered signal:  ",round(opt1,3))
print("Integral after cutoff of original signal:  ",round(o2,3))
print("Integral after cutoff of filtered signal:",round(opt2,3))              
print("Ratio of components after cutoff to before the cutoff of original signal:  ", round(o2/o1,3))
print("Ratio of components after cutoff to before the cutoff of filtered signal:  ",round(opt2/opt1,3))    
