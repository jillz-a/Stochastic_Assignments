import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(1)
rooms = [1, 2, 3, 4, 5]
PI = np.array([[0, 0.5, 0.5, 0, 0],
               [1/3, 0, 1/3, 1/3, 0],
               [0.25, 0.25, 0, 0.25, 0.25],
               [0, 1/3, 1/3, 0, 1/3],
               [0, 0, 0.5, 0.5, 0]])

# Strategy based on the total time distribution
# PI_drone = np.array([[0, 0.32, 0.68, 0, 0],
#                     [0.16, 0, 0.48, 0.36, 0],
#                     [0.19, 0.26, 0, 0.42, 0.13],
#                     [0, 0.27, 0.59, 0, 0.14],
#                     [0, 0, 0.51, 0.49, 0]])

# Strategy based on the caught distribution
# PI_drone = np.array([[0, 0.39, 0.61, 0, 0],
#                     [0.19, 0, 0.66, 0.15, 0],
#                     [0.28, 0.39, 0, 0.22, 0.11],
#                     [0, 0.26, 0.67, 0, 0.07],
#                     [0, 0, 0.82, 0.18, 0]])

# Strategy based on the visit distribution
PI_drone = np.array([[0, 0.27, 0.73, 0, 0],
                    [0.1, 0, 0.5, 0.4, 0],
                    [0.12, 0.21, 0, 0.46, 0.21],
                    [0, 0.22, 0.57, 0, 0.21],
                    [0, 0, 0.56, 0.44, 0]])

# PI_drone = PI

# Assignment 1.3 E
PI_6 = np.linalg.matrix_power(PI, 6)

X_6 = [PI_6[1, 0], PI_6[1, 1], PI_6[1, 2], PI_6[1, 3], PI_6[1, 4]]

# Assignment 1.3 F
# start Monte Carlo simulation
iteration = 0
time_caught = []
average_time_caught = []
simulations = []
temp_time = []
temp_caught = []
room_caught = []
room_visits = [0, 0, 0, 0, 0]
room_times = [0, 0, 0, 0, 0]
while iteration < 500:
    simulations.append(iteration)
    iteration += 1
    init_state_intruder = 5
    init_state_drone = 1

    room_intruder = init_state_intruder
    room_drone = init_state_drone

    t_drone = 0
    t_intruder = 0

    drone_state = np.array([[0], [init_state_drone]])
    intruder_state = np.array([[0], [init_state_intruder]])

    found = False

    while found == False:

        # drone movement:

        t_drone += 1
        room_drone = np.random.choice(rooms, p=PI_drone[room_drone-1])
        drone_state = np.append(drone_state, [[t_drone], [room_drone]], axis = 1)

        # intruder movement

        lam = np.sqrt((2*room_intruder+1)/5)
        t_intruder += np.random.exponential(scale=1/lam)
        room_intruder = np.random.choice(rooms, p=PI[room_intruder-1])
        intruder_state = np.append(intruder_state, [[t_intruder], [room_intruder]], axis = 1)
        # intruder_state[0] = np.append(intruder_state[0], t_intruder)
        # intruder_state[1] = np.append(intruder_state[1], room_intruder)

        for t_d in range(len(drone_state[0])-1):
            for t_i in range(len(intruder_state[0])-1):
                if drone_state[0][t_d] <= intruder_state[0][t_i] <= drone_state[0][t_d+1]:
                    if drone_state[1][t_d] == intruder_state[1][t_i]:
                        temp_time.append(intruder_state[0][t_i])
                        temp_caught.append(intruder_state[1][t_i])
                        found = True
                        print('ITERATION', iteration)
                        print('Drone movement:', drone_state)
                        print('Intruder movement:', intruder_state)
                        print('Intruder found in room', intruder_state[1][t_i], 'at time', intruder_state[0][t_i])

                elif intruder_state[0][t_i] <= drone_state[0][t_d] <= intruder_state[0][t_i+1]:
                    if drone_state[1][t_d] == intruder_state[1][t_i]:
                        temp_time.append(float(drone_state[0][t_d]))
                        temp_caught.append(intruder_state[1][t_i])
                        found = True
                        print('ITERATION', iteration)
                        print('Drone movement:', drone_state)
                        print('Intruder movement:', intruder_state)
                        print('Intruder found in room', intruder_state[1][t_i], 'at time', drone_state[0][t_d])

        if len(temp_time) > 0:
            time_caught.append(min(temp_time))
            average_time_caught.append(np.mean(time_caught))

            if len(temp_caught) > 0:
                if min(temp_time) in drone_state[0]:
                    index = np.where(drone_state[0] == min(temp_time))
                    r = drone_state[1][index[0][0]]
                elif min(temp_time) in intruder_state[0]:
                    index = np.where(intruder_state[0] == min(temp_time))
                    r = intruder_state[1][index[0][0]]
                room_caught.append(r)
                temp_caught.clear()

            temp_time.clear()

    for i in range(len(intruder_state[0])-1):
        caught = 10 # dummy value
        if len(temp_time) > 0:
            caught = min(temp_time)
        room = int(intruder_state[1][i])
        room_visits[room-1] += 1
        time_intr_lst = intruder_state[0]
        if time_intr_lst[i+1] > caught:
            continue
        elif time_intr_lst[i+1] == caught:
            time_intr = time_intr_lst[i+1] - time_intr_lst[i]
        elif time_intr_lst[i+1] < caught:
            time_intr = time_intr_lst[i + 1] - time_intr_lst[i]
        elif time_intr_lst[i] < caught < time_intr_lst[i+1]:
            time_intr = caught - time_intr_lst[i]
        room_times[room-1] += time_intr

print('Number of room visits', room_visits)
print('Total time per room', room_times)
avg_room_times = [i/j for i, j in zip(room_times, room_visits)]
print('Expected time for each room:', avg_room_times)
print('Expected time until caught:', np.mean(time_caught))

sns.histplot(room_caught, binwidth=1, discrete=True, shrink=0.8)
plt.xlabel('Room number')
plt.ylabel('Amount of times caught')
plt.show()
ax = sns.histplot(time_caught, binwidth=0.1)
plt.setp(ax, xticks=[0,1,2,3,4,5,6,7,8,9,10])
plt.xlabel('Time spent by the intruder until it is caught [min]')
plt.show()
# print(room_times)
plt.plot(simulations, average_time_caught)
plt.xlabel('Number of simulation runs')
plt.ylabel('Average time until caught [min]')
plt.show()
x = [1, 2, 3, 4, 5]
room_visits[4] += -500
plt.bar(x, room_visits)
plt.xlabel('Room number')
plt.ylabel('Number of visits')
plt.show()
plt.bar(x, room_times)
plt.xlabel('Room number')
plt.ylabel('Total time')
plt.show()
plt.bar(x, avg_room_times)
plt.xlabel('Room number')
plt.ylabel('Average time')
plt.show()


