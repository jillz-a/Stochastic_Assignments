import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

'''
Assignment 2.1 AE4426-19 Stochastic Processes and Simulation
Code written by Jilles Andringa & Mitchell de Keijzer
'''
iterations = 0

avg_wait_time = []
wait_time = []  # time a passenger needs to wait

#Monte Carlo simulation
while iterations < 2000:
    iterations += 1

    #setup intial values
    pax_que = [] #passenger que, contains arrival times if all desks are full
    desks = [0,0,0] #available desks, 0 if available, pax_arrival if not
    pax_arrival = 0 #passenger arrival time
    time = 0 #starting time


    while time <= 180: #set the time interval in minutes
        pax_arrival += np.random.exponential(1/2.5) #calculate the sojourn time for when next passenger arrives
        pax_que.append(pax_arrival)

        if any(desk != 0 for desk in desks):
            first_desk = min(desk for desk in desks if desk != 0)
            time = min(pax_arrival, first_desk)
        else:
            time = pax_arrival

        for i in range(len(desks)): #check if desk has become available
            if pax_arrival >= desks[i]:
                desks[i] = 0 #reset desk to available

        if any(desk == 0 for desk in desks) and len(pax_que) != 0: #check for available desks
            for i in range(len(desks)):
                if desks[i] == 0 and len(pax_que) != 0: #assign passenger to an available desk
                    # print('Desk', i, 'is available')
                    desks[i] = time + np.random.exponential(1) #time when desk will become available again
                    pax_que.remove(pax_que[0]) #passenger is removed from the que


        elif all(desk != 0 for desk in desks) and len(pax_que) != 0: #if all desk are full, note the waiting time
            # print('All desks are full')
            wait_time.append(abs(min(desks) - pax_que[0]))

    if len(wait_time) != 0:
        avg_wait_time.append(np.average(wait_time))


plt.plot(avg_wait_time)
plt.show()