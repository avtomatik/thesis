import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
fs       =  10e3
N        =  1e5
amp      =  2*np.sqrt(2)
freq     =  1234.0
noise_power  =  0.001*fs/2
time  =  np.arange(N)/fs
x  =  amp*np.sin(2*np.pi*freq*time)
x + =  np.random.normal(scale  =  np.sqrt(noise_power),  size  =  time.shape)
f,  Pxx_den  =  signal.periodogram(x,  fs)
##plt.semilogy(f,  Pxx_den)
##plt.ylim([1e-7,  1e2])
##plt.xlabel("frequency [Hz]")
##plt.ylabel("PSD [V**2/Hz]")
print("{:, .7f}".format(np.mean(Pxx_den[256:])))
f,  Pxx_spec  =  signal.periodogram(x,  fs,  "flattop",  scaling  =  "spectrum")
plt.figure()
plt.semilogy(f,  np.sqrt(Pxx_spec))
plt.ylim([1e-4,  1e1])
plt.xlabel("frequency [Hz]")
plt.ylabel("Linear Spectrum [V RMS]")
print("{:, .7f}".format(np.sqrt(Pxx_spec.max())))
plt.show()