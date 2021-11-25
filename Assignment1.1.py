import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(1)
random.seed(1)
#E-vtol assignment

X = [1, 2, 3, 4, 5, 6]
prob_dist = [0.01, 0.2, 0.5, 0.25, 0.03, 0.01]
t_start = 9 * 60
t_end = 11 * 60
sep = 3
vtols = 12

#check amount of simulation runs
numb_of_runs = 0
i = []
average = []
runs = []

# while numb_of_runs <= 5000:
#     dist = [0, 0, 0, 0, 0, 0]
#     while sum(dist) < vtols:
#         x = np.random.choice(X, p = prob_dist)
#         dist[X.index(x)] += 1
#
#     #check for x = 2, mean should be 6
#     i.append(dist[2])
#     average.append(np.average(i))
#     runs.append(numb_of_runs)
#     numb_of_runs += 1
#
# plt.plot(runs, average)
# plt.plot(runs, 6* np.ones(len(runs)))
# plt.xlabel('Number of simulation runs')
# plt.ylabel('Average number of e-VTOLs at i = 3')
# plt.show()

#a&b.
# reg_2 = 0
# while numb_of_runs <= 2000:
#     dist = [0, 0, 0, 0, 0, 0]
#     while sum(dist) < vtols:
#         x = np.random.choice(X, p = prob_dist)
#         dist[X.index(x)] += 1
#
#     #check for x = 2, mean should be 6
#     i.append(dist[1])
#     average.append(np.average(i))
#     runs.append(numb_of_runs)
#     if dist[1] > dist[2]:
#       reg2 += 1
#     numb_of_runs += 1
#
# prob_reg2_reg3 = reg2/2000
# print(prob_reg2_reg3)
# print(np.average(average))

#b.
T_delay = []
while numb_of_runs <= 2000:
    numb_of_runs += 1
    t_delay = 0
    arrival_time_dist = []
    for i in range(12):
        arrival_time = random.randrange(t_start, t_end)
        arrival_time_dist.append(arrival_time)

    for i in range(len(arrival_time_dist)-1):
        if abs(arrival_time_dist[i] - arrival_time_dist[i+1]) < sep:
            t_delay += sep - abs(arrival_time_dist[i] - arrival_time_dist[i+1])
    T_delay.append(t_delay)

var = np.var(T_delay)
print(var)
print(np.average(T_delay))
sns.histplot(data = T_delay)
plt.show()
