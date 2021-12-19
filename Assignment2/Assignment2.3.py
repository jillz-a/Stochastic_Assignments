import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

beta = 3
sigma = 5
dt = 0.1
t = 0
x_list = []
var_list = []
Exp = []
runs = []
var = []
iterations = 0
x = 0

# Bt = np.random.normal(0, 3)
# print(Bt)
# Xt = beta * 3 + sigma * Bt

while iterations < 10000:
    Bt = np.random.normal(0, t)
    # Bt = norm.pdf(x)
    x = (beta * t + sigma * Bt)
    # x_list.append(x**2)
    # Exp.append(np.mean(x_list))

    if t == 3:
        runs.append(iterations)
        iterations += 1
        x_list.append(x**2)
        var_list.append(x)
        Exp.append(np.mean(x_list))
        var.append(np.var(var_list))
        x = 0
        t = 0
    t += 1

    # print(x)

plt.plot(runs, Exp)
plt.plot(runs, var)
plt.show()


