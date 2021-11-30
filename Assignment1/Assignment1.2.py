import numpy as np
import pandas as pd
from scipy.special import gamma
import matplotlib.pyplot as plt
import seaborn as sns


gamma_func = []



# for brake in brakes:
#     gamma_func.append(gamma(data[brake]))
#     print(gamma_func)

with open('data.csv', 'r') as f:
    df = pd.read_csv(f, sep=',', header=0)
    data = df.values

n = 8
alpha = np.linspace(0.001, 1, 999)
v_brakes = np.zeros((299,8))

for i in range(1,9):
    degradation = data[:,i]
    v_brake = []
    for j in range(len(degradation)-1):
        v = degradation[j+1] - degradation[j]

        if v <= -0.95:
            v = 0

        v_brake.append(v)
    v_brakes[:,i-1] = v_brake


v_total = np.concatenate(v_brakes)
v_total = v_total[v_total != 0.0]
# sns.histplot(v_total)

likelihood = n*(alpha - 1)*sum([np.log(y) for y in v_total])/n - n*alpha - n*alpha*np.log(gamma(alpha)) - n*alpha*np.log(sum(v_total)/n) + n*alpha*np.log(alpha)
plt.plot(alpha, likelihood)

plt.show()