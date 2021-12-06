import numpy as np

rooms = [1,2,3,4,5]
PI = np.array([[0, 0.5, 0.5, 0, 0],
               [1/3, 0, 1/3, 1/3, 0],
               [0.25, 0.25, 0, 0.25, 0.25],
               [0, 1/3, 1/3, 0, 1/3],
               [0, 0, 0.5, 0.5, 0]])

#Assignemnt 1.3 E
PI_6 = np.linalg.matrix_power(PI, 6)

X_6 = [PI_6[1,0] , PI_6[1,1], PI_6[1,2], PI_6[1,3], PI_6[1,4]]

#Assignment 1.3 F
#start Monte Carlo simulation
iteration = 0
while iteration < 5:
    iteration += 1
    init_state_intruder = 1
    init_state_drone = 5

    room_intruder = init_state_intruder
    room_drone = init_state_drone

    t_drone = 0
    t_intruder = 0

    drone_state = np.array([[0], [init_state_drone]])
    intruder_state = np.array([[0], [init_state_intruder]])

    found = False

    while found == False:

        #drone movement:

        t_drone += 1
        room_drone = np.random.choice(rooms, p=PI[room_drone-1])
        drone_state = np.append(drone_state, [[t_drone], [room_drone]], axis = 1)


        #intruder movement

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
                        found = True
                        print('Drone movement:', drone_state)
                        print('Intruder movement:', intruder_state)
                        print('Drone found in room', intruder_state[1][t_i], 'at time', intruder_state[0][t_i])

                elif intruder_state[0][t_i] <= drone_state[0][t_d] <= intruder_state[0][t_i+1]:
                    if drone_state[1][t_d] == intruder_state[1][t_i]:
                        found = True
                        print('Drone movement:', drone_state)
                        print('Intruder movement:', intruder_state)
                        print('Drone found in room', intruder_state[1][t_i], 'at time', drone_state[0][t_d])