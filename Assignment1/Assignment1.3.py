import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(1)
rooms = [1,2,3,4,5]
PI = np.array([[0, 0.5, 0.5, 0, 0],
               [1/3, 0, 1/3, 1/3, 0],
               [0.25, 0.25, 0, 0.25, 0.25],
               [0, 1/3, 1/3, 0, 1/3],
               [0, 0, 0.5, 0.5, 0]])

PI_drone = np.array([[0, 0.3, 0.7, 0, 0],
                    [0.15, 0, 0.5, 0.35, 0],
                    [0.15, 0.2, 0, 0.3, 0.35],
                    [0, 0.2, 0.4, 0, 0.4],
                    [0, 0, 0.6, 0.4, 0]])
# PI_drone = np.array([[0, 0.3, 0.7, 0, 0],
#                     [0, 0, 0.7, 0.3, 0],
#                     [0, 0, 0.5, 0.5, 0],
#                     [0, 0, 0.5, 0.5, 0],
#                     [0, 0, 0.6, 0.4, 0]])

# PI_drone = PI
#Assignemnt 1.3 E
PI_6 = np.linalg.matrix_power(PI, 6)

X_6 = [PI_6[1,0] , PI_6[1,1], PI_6[1,2], PI_6[1,3], PI_6[1,4]]

#Assignment 1.3 F
#start Monte Carlo simulation
iteration = 0
time_caught = []
average_time_caught = []
simulations = []
temp_time = []
room_visits = [0, 0, 0, 0, 0]
room_times = [0, 0, 0, 0, 0]
while iteration < 500:
    simulations.append(iteration)
    iteration += 1
    init_state_intruder = 5
    init_state_drone = 2

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
                        found = True
                        print('ITERATION', iteration)
                        print('Drone movement:', drone_state)
                        print('Intruder movement:', intruder_state)
                        print('Intruder found in room', intruder_state[1][t_i], 'at time', intruder_state[0][t_i])
                        # time_caught.append(intruder_state[0][t_i])
                        # average_time_caught.append(np.mean(time_caught))

                elif intruder_state[0][t_i] <= drone_state[0][t_d] <= intruder_state[0][t_i+1]:
                    if drone_state[1][t_d] == intruder_state[1][t_i]:
                        temp_time.append(float(drone_state[0][t_d]))
                        found = True
                        print('ITERATION', iteration)
                        print('Drone movement:', drone_state)
                        print('Intruder movement:', intruder_state)
                        print('Intruder found in room', intruder_state[1][t_i], 'at time', drone_state[0][t_d])
                        # time_caught.append(float(drone_state[0][t_d]))
                        # average_time_caught.append(np.mean(time_caught))
        if len(temp_time) > 0:
            time_caught.append(min(temp_time))
            average_time_caught.append(np.mean(time_caught))
            temp_time.clear()

    for i in range(len(intruder_state[0])-1):
        # print('tst', intruder_state[1][i])
        caught = 10
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
        # print('test', time_intr_lst)
        room_times[room-1] += time_intr


print(room_visits)
print(room_times)
avg_room_times = [i/j for i,j in zip(room_times,room_visits)]
print(avg_room_times)
print(np.mean(time_caught))
# sns.histplot(time_caught)
# print(room_times)
plt.plot(simulations, average_time_caught)
plt.show()
x = [1,2,3,4,5]
plt.bar(x, room_times)
plt.show()
plt.bar(x, avg_room_times)
plt.show()


