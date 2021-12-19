import numpy as np
import matplotlib.pyplot as plt

'''
Assignment 2.2 AE4426-19 Stochastic Processes and Simulation
Code written by Jilles Andringa & Mitchell de Keijzer

Variables:
X_t: The true condition of the machinery at time t
Y_t: The measured degradation condition of the machinery at time t
V_t: A sequence of i.i.d. Gaussian random variables independent of X_t, X_(t-1), ..., X_0
e_t: measurement error, independent of e_(t-1), ..., e_0.

'''

np.random.seed(1)

# 2b&c
iterations = 0
runs = []
A = np.array([[1, 0], [1, 1]])
B = np.array([[1], [0.1]])
C = np.array([1, 1])
X_t = np.array([[0], [0]]) # = X_0
t = 0
times = [] # lists all first times when the measured level of degradation exceeds L=1000
average_time = []
Yt_list = [] # lists all Y_t values at t=30
Exp_Yt = [] # gives the average of all current Y_t values in Yt_list

# Monte carlo simulation
while iterations < 2000:
    V_t = np.array([[np.random.normal(0, 1)], [np.random.normal(0, 1)]])
    e_t = np.random.normal(0, 0.1)
    Y_t = np.matmul(C, X_t) + e_t
    X_t = np.matmul(A, X_t) + B + V_t
    if t == 30:
        Yt_list.append(Y_t)
        Exp_Yt.append(np.mean(Yt_list))
    if Y_t >= 1000:
        times.append(t)
        average_time.append(np.mean(times))
        runs.append(iterations)
        iterations += 1
        X_t = np.array([[0], [0]])
        t = -1
    t += 1
print('L=1000 exceeded at time', np.mean(times))
plt.plot(runs, average_time)
plt.xlabel("Simulation runs")
plt.ylabel("Time")
plt.show()

# 2c
print('Expected level of degradation at t=30:', np.mean(Yt_list))
plt.plot(runs, Exp_Yt)
plt.xlabel("Simulation runs")
plt.ylabel("Measured level of degradation")
plt.show()

