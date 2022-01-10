import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from Definitions import mean_confidence_interval

'''
Assignment 2.1 AE4426-19 Stochastic Processes and Simulation
Code written by Jilles Andringa & Mitchell de Keijzer
'''
iterations = 0

wait_time = []  # time a passenger needs to wait
avg_wait_time = [] # average time a passenger needs to wait

#Monte Carlo simulation
while iterations < 1500:
    iterations += 1

    #setup intial values
    time = 0        # starting time
    pax_que = []    # passenger que, contains passenger arrival times
    desks = [0,0,0] # available desks, 0 if available, pax_arrival if not
    pax_arrival = 0 # passenger arrival time


    while time <= 180:  # set the time interval in minutes
        pax_arrival += np.random.exponential(1/2.5) # calculate the sojourn time for when next passenger arrives
        pax_que.append(pax_arrival)

        # Variable time step, check what happens first, desk becomes available or new passenger arrives
        if any(desk != 0 for desk in desks):
            first_desk = min(desk for desk in desks if desk != 0) # first desk that will become available
            time = min(pax_arrival, first_desk)
        else:
            time = pax_arrival

        # check if desk has become available
        for i in range(len(desks)):
            if time >= desks[i]:
                desks[i] = 0 # reset desk to available

        # check for available desks
        if any(desk == 0 for desk in desks) and len(pax_que) != 0 and time >= pax_que[0]:
            for i in range(len(desks)):
                if desks[i] == 0 and len(pax_que) != 0:         # assign passenger to an available desk
                    desks[i] = time + np.random.exponential(1)  # time when desk will become available again
                    pax_que.remove(pax_que[0])                  # passenger is removed from the que

        # if all desk are full, note the waiting time
        if all(desk != 0 for desk in desks) and len(pax_que) != 0 and time >= pax_que[0]:
            wait_time.append(abs(min(desks) - pax_que[0]))

    if len(wait_time) != 0:
        avg_wait_time.append(np.average(wait_time))

# plotting
plt.plot(avg_wait_time)
plt.ylabel('Waiting time in minutes')
plt.xlabel('Iterations')
plt.show()

sns.histplot(wait_time)
plt.xlabel('Waiting time in minutes')
plt.show()

# confidence intervals of waiting time
m, m_min, m_plus = mean_confidence_interval(wait_time)
print(m, m-m_min, m-m_plus)