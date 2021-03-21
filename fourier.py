#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22

@author: robin
"""
import numpy as np
from cossin import cos, sin, ind


def goertzel(x,k):
    N   = np.size(x)
    A   = 2*np.pi*k/N
    B   = 2*np.cos(A)
    y1  = 0
    y2  = 0
    for n in range(N):
        y0 = x[n]+y1*B-y2
        y2 = y1
        y1 = y0
    if k > 0:
        y0 = 2*np.hypot(y1-y2*0.5*B,y2*np.sin(A))/N
    else:
        y0 = np.hypot(y1-y2*0.5*B,y2*np.sin(A))/N
    return y0

def dft_p(x):
    N   = np.size(x)
    M   = M = np.zeros([N,N],dtype=complex)
    F   = np.zeros(N,dtype=complex)
    for k in range(N):
        for n in range(N):
            M[n][k] = np.exp(-2j*np.pi*k*n/N)
            F[k] = F[k] + x[n]*np.exp(-2j*np.pi*k*n/N)
        if k > 0:    
            F[k] = 2*F[k]    
        if k > k/2:
            F[k] = 0
    return abs(F)/N

def dft_c(x):
    N   = np.size(x)
    A   = np.zeros(N)
    B   = np.zeros(N)
    F   = np.zeros(N)
    for k in range(N):
        for n in range(N):                          
            A[k] = A[k] + x[n]*np.int8(np.round(100*np.cos(2*np.pi*k*n/N)))
            B[k] = B[k] + x[n]*np.int8(np.round(100*np.sin(2*np.pi*k*n/N))) 
            F[k] = np.hypot(A[k],B[k])   
        if k > 0:    
            F[k] = 2*F[k]    
    return abs(F/N)/100


def cooley_tukey_p(x):
	N = len(x) 
	if N <= 1:
		return x
	even = cooley_tukey_p(x[0::2])
	odd =  cooley_tukey_p(x[1::2])
	temp = [i for i in range(N)]
	for k in range(N//2):
		temp[k] = even[k] + np.exp(-2j*np.pi*k/N) * odd[k]
		temp[k+N//2] = even[k] - np.exp(-2j*np.pi*k/N)*odd[k]            
	return temp

def fft_p(x):
    N    = np.size(x)
    F    = np.zeros(N)
    X    = cooley_tukey_p(x)
    F[0] = np.abs(X[0])/N
    for i in range(1,N,1):
        if i < N/2:
            F[i] = 2*np.abs(X[i])/N
        else:
            F[i] = 0
    return F

def cooley_tukey_c(x):
	N = len(x)
	if N <= 1:
		temp = np.zeros([N,2])
		temp[0,0] = x
		return temp
	even = cooley_tukey_c(x[0::2])
	odd =  cooley_tukey_c(x[1::2])
	temp = np.zeros([N,2])
	comp = np.zeros([1,2])
	i = ind[N]-1
	for k in range(int(N/2)):
		c = cos[i][k]
		s = sin[i][k]
		comp[0,0] = c * odd[k,0] + s * odd[k,1]
		comp[0,1] = c * odd[k,1] - s * odd[k,0]
		temp[k,0] = even[k,0] + comp[0,0]
		temp[k,1] = even[k,1] + comp[0,1]
		temp[k+N//2,0] = even[k,0] - comp[0,0]
		temp[k+N//2,1] = even[k,1] - comp[0,1]
	return temp

def fft_c(x):
    N    = np.size(x)
    F    = np.zeros(N)
    X    = cooley_tukey_c(x)
    F[0] = np.hypot(X[0,0],X[0,1])/N
    for i in range(1,N,1):
        F[i] = 2*np.hypot(X[i,0],X[i,1])/N
    return F
    
def idft_p(x):
    N   = np.size(x)
    F   = np.zeros(N,dtype=complex)
    for k in range(N):
        for n in range(N):
            F[k] = F[k] + x[n]*np.exp(2j*np.pi*k*n/N)
        if k > 0:    
            F[k] = 2*F[k]    
        if k > k/2:
            "F[k] = 0"
    return abs(F)/N

def ifft_p(x):
    N    = np.size(x)
    F    = np.zeros(N)
    X    = icooley_tukey_p(x)
    F[0] = np.abs(X[0])/N
    for i in range(1,N,2):
        F[i] = 2*np.abs(X[i])/N
    return F

def icooley_tukey_p(x):
	N = len(x) 
	if N <= 1:
		return x
	even = cooley_tukey_p(x[0::2])
	odd =  cooley_tukey_p(x[1::2])
	temp = [i for i in range(N)]
	for k in range(N//2):
		temp[k] = even[k] + np.exp(2j*np.pi*k/N) * odd[k]
		temp[k+N//2] = even[k] - np.exp(2j*np.pi*k/N)*odd[k]            
	return temp

def ifft_c(x):
    N    = np.size(x)
    F    = np.zeros(N)
    X    = icooley_tukey_c(x)
    F[0] = np.hypot(X[0,0],X[0,1])/N
    for i in range(1,N):
        F[i] = 0.5*np.hypot(X[i,0],X[i,1])
    return F

def icooley_tukey_c(x):
	N = len(x)
	if N <= 1:
		temp = np.zeros([N,2])
		temp[0,0] = x
		return temp
	even = cooley_tukey_c(x[0::2])
	odd =  cooley_tukey_c(x[1::2])
	temp = np.zeros([N,2])
	comp = np.zeros([1,2])
	i = ind[N]-1
	for k in range(int(N/2)):
		c = cos[i][k]
		s = sin[i][k]
		comp[0,0] = c * odd[k,0] - s * odd[k,1]
		comp[0,1] = c * odd[k,1] + s * odd[k,0]
		temp[k,0] = even[k,0] + comp[0,0]
		temp[k,1] = even[k,1] + comp[0,1]
		temp[k+N//2,0] = even[k,0] - comp[0,0]
		temp[k+N//2,1] = even[k,1] - comp[0,1]
	return temp