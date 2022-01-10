import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from Definitions import mean_confidence_interval

'''
Assignment 2.1 f AE4426-19 Stochastic Processes and Simulation
Code written by Jilles Andringa & Mitchell de Keijzer
'''
iterations = 0

wait_time = []  # time a passenger needs to wait
bsns_wait_time = [] #time business passenger needs to wait
avg_wait_time = [] # average time a passenger needs to wait
avg_bsns_wait_time = [] #average time a buisness passenger needs to wait
amount_of_pax = [] #total amount of passengers who entered the que for every iteration
amount_of_bsns = [] #total amount of business passengers who entered the que for every iteration

#Monte Carlo simulation
while iterations <= 1500:
    iterations += 1

    #setup intial values
    time = 0  # starting time
    pax_que = [] #passenger que, contains passenger arrival times
    bsns_que = [] #buisness passenger que, contains passenger arrival times
    desks = [0,0,0] #available desks, 0 if available, pax_arrival if not
    pax_arrival = 0 #passenger arrival time
    bsns_arrival = 0 #buisness passenger arrival time
    pax_amount = 0 #total amount of passengers who entered the que
    bsns_amount = 0 #total amount of passengers who entered the que

    while time <= 180: #set the time interval in minutes
        # calculate the sojourn time for when next (business) passenger arrives
        if pax_arrival < 180:
            pax_arrival += np.random.exponential(1/2)
            pax_amount += 1
            pax_que.append(pax_arrival)
        if bsns_arrival < 180:
            bsns_arrival += np.random.exponential(1/0.5)
            bsns_amount += 1
            bsns_que.append(bsns_arrival)

        #Variable time step, check what happens first, desk becomes available or new passenger arrives
        if any(desk != 0 for desk in desks):
            first_desk = min(desk for desk in desks if desk != 0) #first desk that will become available
            time = min(pax_arrival, bsns_arrival, first_desk)
        else:
            time = min(pax_arrival, bsns_arrival)

        # check if desk has become available between time steps
        for i in range(len(desks)):
            if time >= desks[i]:
                desks[i] = 0 #reset desk to available

        # check for available desks for business passengers
        if any(desk == 0 for desk in desks) and len(bsns_que) != 0:
            for i in range(len(desks)):
                if desks[i] == 0 and len(bsns_que) != 0 and time >= bsns_que[0]:  # assign business passenger to an available desk
                    desks[i] = time + np.random.exponential(1)  # time when desk will become available again
                    bsns_que.remove(bsns_que[0])  # passenger is removed from the que

        # if all desk are full, note the waiting time
        if all(desk != 0 for desk in desks) and len(bsns_que) != 0 and time >= bsns_que[0]:
            bsns_wait_time.append(abs(min(desks) - bsns_que[0]))

        # check for available desks for normal passengers
        if any(desk == 0 for desk in desks) and len(pax_que) != 0 and time >= pax_que[0]:
            for i in range(len(desks)):
                if desks[i] == 0 and len(pax_que) != 0: #assign passenger to an available desk
                    desks[i] = time + np.random.exponential(1) #time when desk will become available again
                    pax_que.remove(pax_que[0]) #passenger is removed from the que

        # if all desk are full, note the waiting time
        if all(desk != 0 for desk in desks) and len(pax_que) != 0 and time >= pax_que[0]:
            wait_time.append(abs(min(desks) - pax_que[0]))

    #add wait times and passenger counts to lists
    amount_of_pax.append(pax_amount)
    amount_of_bsns.append(bsns_amount)
    if len(wait_time) != 0:
        avg_wait_time.append(np.average(wait_time))
    if len(bsns_wait_time) != 0:
        avg_bsns_wait_time.append(np.average(bsns_wait_time))


plt.plot(avg_wait_time)
plt.plot(avg_bsns_wait_time)
plt.ylabel('Average waiting time in minutes')
plt.xlabel('Iterations')
plt.show()

sns.histplot(wait_time, color= 'g')
sns.histplot(bsns_wait_time, color = 'r')
plt.xlabel('Waiting time in minutes')
# plt.xlim(0, 50)
plt.show()

m, m_min, m_plus = mean_confidence_interval(wait_time)
print('passenger average wait time:', m, m-m_min, m-m_plus)

m, m_min, m_plus = mean_confidence_interval(bsns_wait_time)
print('business passenger average wait time:', m, m-m_min, m-m_plus)

