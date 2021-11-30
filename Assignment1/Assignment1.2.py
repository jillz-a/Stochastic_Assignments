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


v_brakes = np.concatenate(v_brakes)
v_brakes = v_brakes[v_brakes != 0.0]
sns.histplot(v_brakes)

plt.show()