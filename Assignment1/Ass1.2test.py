test = 1
test2 = 1 + test

print(test2)

#b
numb_of_runs = 0
i = []
average = []
runs = []
X = [181, 168, 141, 227, 163, 128, 276, 171]
prob_dist = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
while numb_of_runs <= 5000:


    dist = [0, 0, 0, 0, 0, 0]
    while sum(dist) < vtols:
        x = np.random.choice(X, p = prob_dist)
        dist[X.index(x)] += 1

    #check for x = 2, mean should be 6
    i.append(dist[2])
    average.append(np.average(i))
    runs.append(numb_of_runs)
    numb_of_runs += 1
