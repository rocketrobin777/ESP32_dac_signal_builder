#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22

@author: robin
"""
from fourier import dft_c,dft_p,fft_p,fft_c, goertzel
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

N   = 512
f   = 50
w   = 2*f*np.pi
phase = 0*np.pi/180;
n   = 1024
t   = np.arange(0,1/f,1/(f*n))
y   = 128
y   = y + 128*np.sin(w*t+phase)
y   = y + 0*np.sin(2*(w*t+phase))
y   = y + 50*np.sin(3*(w*t+phase))
y   = y + 0*np.sin(5*(w*t+phase))
y   = y + 0*np.sin(7*(w*t+phase))

td  = np.arange(0,1/f,1/(f*N))
yd  = np.zeros(N)
for i in range(N):
    yd[i] = np.uint8(np.round((y[t.tolist().index(td[i])])))

yd = yd-min(yd)
print("min = "+str(min(yd)))
print("max = "+str(max(yd)))
f   = f*np.arange(0,N,1)

##############################################################################
t = t*1e3
td = td*1e3
title_font = {'fontname':'Arial', 'size':'24', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'}
lable_font = {'fontname':'Arial', 'size':'20', 'color':'black', 'weight':'normal'}
mpl.rcParams['xtick.labelsize'] = 18
mpl.rcParams['ytick.labelsize'] = 18
mpl.rcParams['lines.linewidth'] = 3
mpl.rcParams['lines.markersize'] = 14

plt.figure()
plt.plot(t,y,'k',td,yd,'ro')
plt.xlim(0,20)
plt.ylim(min(y)-0.5,max(y)+0.5)
plt.title('Signal time domain',**title_font)
plt.xlabel("t [ms]",**lable_font)
plt.grid()
plt.show()

F1   = fft_c(yd)
plt.figure()
plt.stem(f,F1,'k',use_line_collection = True)
plt.title('Signal freqency domain with FFT',**title_font)
plt.xlabel("f [Hz]",**lable_font)
plt.grid()
plt.show()

file = open("Signal.h", "w")
file.write("uint8_t buf["+str(N)+"] = {\n")
for k in range(0,N):
 	file.write(str(np.uint8(yd[k]))+",")
 	if np.mod(k+1,4) == 0:
         file.write("\n")
file.write("};")
file.close()
