import numpy as np

'''
Assignment 2.1 AE4426-19 Stochastic Processes and Simulation
Code written by Jilles Andringa & Mitchell de Keijzer
'''

#setup intial values
pax_que = [] #passenger que, contains arrival times if all desks are full
desks = [0, 0, 0] #available desks, 0 if available, pax_arrival if not
pax_arrival = 0 #passenger arrival time


while pax_arrival < 180:
    pax_arrival += np.random.poisson(2.5)

    if any(desk == 0 for desk in desks):
        for i in range(len(desks)):
            if desks[i] == 0:
                desks[i] = np.random.exponential(1)

    else:
        pax_que.append(pax_arrival)