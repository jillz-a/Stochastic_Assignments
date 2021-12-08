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
sns.histplot(v_total, binwidth=0.003)

plt.show()

n = len(v_total)
alpha = np.linspace(0.001, 1, 999)

likelihood = n*(alpha - 1)*sum([np.log(y) for y in v_total])/n - n*alpha - n*np.log(gamma(alpha)) - n*alpha*np.log(sum(v_total)/n) + n*alpha*np.log(alpha)
plt.plot(alpha, likelihood)
plt.xlabel('alpha')
plt.ylabel('Likelihood')

#acquried coefficients
alpha_max = alpha[np.where(likelihood == max(likelihood))]
beta = (sum(v_total)/n) / alpha_max
print('alpha found =', alpha_max)
print('beta found =', beta)

#given coefficients
alpha_max = 0.2
beta = 0.02

print('alpha used = ',alpha_max)
print('beta used = ',beta)

plt.axvline(x = alpha_max, label = 'MLE alpha', color = 'r')
plt.show()

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
plt.show()

mean = np.mean(MTTF)
var = np.var(MTTF)

CI = (mean - 1.96 * np.sqrt(var / 5000), mean + 1.96 * np.sqrt(var / 5000))
print('Mean Time To Failure:', mean)
print('Confidence Interval:', CI)


#b & c
iteration = 0
cycles = 0
X_i = 0
X_i_lst = []
unscheduled_cycles = []
lst_200 = []
lst_250 = []
while iteration <= 5000:
    cycles += 1
    v = np.random.gamma(alpha_max, beta)
    X_i += v
    if X_i > 1:
        if cycles < 200:
            unscheduled_cycles.append(cycles)
        X_i_lst.append(X_i)
        iteration += 1
        cycles = 0
        X_i = 0
    if cycles == 200:
        lst_200.append(X_i)
    if cycles == 250:
        lst_250.append(X_i)
        X_i_lst.append(X_i)
        iteration += 1
        cycles = 0
        X_i = 0

prob = len(lst_250)/len(lst_200)
print('Probability of 250 cycles without failing:', prob)

scheduled = len([i for i in lst_200 if i <= 1.0])
unscheduled = len(unscheduled_cycles)
ratio = unscheduled / scheduled
mean_unscheduled = np.mean(unscheduled_cycles)
print('Unscheduled against schedules replacements ratio:', ratio)
print('Mean number of flight cycles unscheduled:', mean_unscheduled)

mean = np.mean(X_i_lst)
var = np.var(X_i_lst)
CI = (mean - 1.96 * np.sqrt(var / 5000), mean + 1.96 * np.sqrt(var / 5000))
print('Mean Time To Failure:', mean)
print('Confidence Interval:', CI)


