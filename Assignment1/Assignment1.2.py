import numpy as np
import pandas as pd
from scipy.special import gamma

data = pd.read_csv(open('data.csv', 'r'))
brakes = ['Brake-1', 'Brake-2', 'Brake-3', 'Brake-4', 'Brake-5', 'Brake-6', 'Brake-7', 'Brake-8']

gamma_func = []

print(gamma(list(data['Brake-1'])))

# for brake in brakes:
#     gamma_func.append(gamma(data[brake]))
#     print(gamma_func)

