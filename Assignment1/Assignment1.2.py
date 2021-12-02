import numpy as np
import pandas as pd
from scipy.special import gamma
import matplotlib.pyplot as plt
import seaborn as sns


gamma_func = []


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


v_total = np.concatenate(v_brakes)
v_total = v_total[v_total != 0.0]
# sns.histplot(v_total, binwidth=0.003)

# plt.show()

n = len(v_total)
alpha = np.linspace(0.001, 1, 999)

likelihood = n*(alpha - 1)*sum([np.log(y) for y in v_total])/n - n*alpha - n*np.log(gamma(alpha)) - n*alpha*np.log(sum(v_total)/n) + n*alpha*np.log(alpha)
# plt.plot(alpha, likelihood)
# plt.xlabel('alpha')
# plt.ylabel('Likelihood')

#acquried coefficients
alpha_max = alpha[np.where(likelihood == max(likelihood))]
beta = (sum(v_total)/n) / alpha_max

#given coefficients
alpha_max = 0.2
beta = 0.02

print('alpha = ',alpha_max)
print('beta = ',beta)

# plt.axvline(x = alpha_max, label = 'MLE alpha', color = 'r')

#Calculate mean time to failure using alpha and beta
iteration = 0
cycles = 0
X_i = 0
MTTF = [] #Mean Time To Failure list
MTTF_avg = []
while iteration <= 5000:
    cycles += 1
    v = np.random.gamma(alpha_max, beta)
    X_i += v
    if X_i >= 1.0:
        MTTF.append(cycles)
        MTTF_avg.append(np.average(MTTF))
        iteration += 1
        cycles = 0
        X_i = 0

plt.plot(MTTF_avg)
plt.xlabel('iterations')
plt.ylabel('Cycles to failure')
# plt.show()

mean = np.mean(MTTF)
var = np.var(MTTF)

CI = (mean - 1.96 * np.sqrt(var / 2000), mean + 1.96 * np.sqrt(var / 2000))
print('Mean Time To Failure:', mean)
print('Confidence Interval:', CI)

iteration = 0
cycles = 0
X_i = 0
X_i_lst = []
while iteration <= 5000:
    cycles += 1
    v = np.random.gamma(alpha_max, beta)
    X_i += v
    if cycles == 250:
        X_i_lst.append(X_i)
        iteration += 1
        cycles = 0
        X_i = 0

prob = len([i for i in X_i_lst if i < 1.0])/len(X_i_lst)
print('Probability of 250 cycles without failing:', prob)
mean = np.mean(X_i_lst)
var = np.var(X_i_lst)

CI = (mean - 1.96 * np.sqrt(var / 2000), mean + 1.96 * np.sqrt(var / 2000))
print('Mean Time To Failure:', mean)
print('Confidence Interval:', CI)