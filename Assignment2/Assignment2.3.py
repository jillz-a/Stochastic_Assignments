import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

'''
Assignment 2.3 AE4426-19 Stochastic Processes and Simulation
Code written by Jilles Andringa & Mitchell de Keijzer

Variables:
X_t: The degradation over time of a component (wearing)
t: time
B_t: standard Brownian motion

Constants:
beta: degradation drift
sigma: diffusion coefficient

'''

np.random.seed(1)

# constants
beta = 3
sigma = 5

# starting values
t = 3 # as asked for in the assignment
SD = np.sqrt(3) # sigma^2 = t - s --> sigma = sqrt(3) for np.random.normal(mu, sigma)
iterations = 0
X_t = 0 # we are considering X_0 = 0

# lists
Xt2_list = [] # list for the (X_3)^2 values
Xt_list = [] # list for the X_3 values
Exp = [] # list for the mean values of the (X_3)^2 values
Var = [] # list for the variance values of the X_3 values
runs = [] # list for the amount of simulation runs


while iterations < 10000:
    Bt = np.random.normal(0, SD)
    X_t = (beta * t + sigma * Bt)
    Xt2_list.append(X_t ** 2)
    Xt_list.append(X_t)
    Exp.append(np.mean(Xt2_list))
    Var.append(np.var(Xt_list))
    runs.append(iterations)
    if iterations == 10:
        print('E[(X_3)^2] at 10 runs:', np.mean(Xt2_list))
        print('Var(X_3) at 10 runs:', np.var(Xt_list))
        plt.subplot(3, 2, 1)
        plt.plot(runs, Var)
        plt.title("Variance")
        plt.subplot(3, 2, 2)
        plt.plot(runs, Exp)
        plt.title("Expectation")
        # plt.xlabel('Simulation run')
        # plt.ylabel('Variance of X_t')
        # plt.show()
    if iterations == 100:
        print('E[(X_3)^2] at 100 runs:', np.mean(Xt2_list))
        print('Var(X_3) at 100 runs:', np.var(Xt_list))
        plt.subplot(3, 2, 3)
        plt.plot(runs, Var)
        plt.ylabel('Variance of X-value for t = 3 [-]')
        plt.subplot(3, 2, 4)
        plt.plot(runs, Exp)
        plt.ylabel('Expectation of the squared X-value for t = 3 [-]')
        # plt.xlabel('Simulation run')

        # plt.show()
    iterations += 1

print('E[(X_3)^2] at 10000 runs = ', np.mean(Xt2_list))
CI = (np.mean(Xt2_list) - 1.96 * np.sqrt(np.var(Xt2_list) / 10000), np.mean(Xt2_list) + 1.96 * np.sqrt(np.var(Xt2_list) / 10000))
print('CI', CI)
print('Var(X_3) at 10000 runs = ', np.var(Xt_list))

plt.subplot(3, 2, 5)
plt.xlabel('Simulation run [-]')
# plt.ylabel('Variance of X_t')
plt.plot(runs, Var)
plt.subplot(3, 2, 6)
plt.xlabel('Simulation run [-]')
plt.plot(runs, Exp)
plt.show()

# plt.plot(runs, Exp)
# plt.xlabel('Simulation run')
# plt.ylabel('Average (X_t)^2 value')
# plt.show()


# plt.hist(Xt_list)
sns.histplot(data=Xt_list, binwidth=1)
plt.xlabel('X-value [-]')
plt.show()

dirac = []
for i in range(len(Xt_list)):
    px = 1 / (i + 1) * Xt_list[i]
    dirac.append(px)

y = np.ones(len(Xt_list))
plt.stem(dirac, y)
plt.show()


