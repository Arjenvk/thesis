import matplotlib.pyplot as plt

## UK
ILP_int = [3.192, 2.050, 1.570, 1.317, 1.288, 1.004, 0.949, 0.851, 0.801, 0.682, 0.672, 0.616, 0.461, 0.446, 0.437]
ILP_comp = [29.16, 761.63, 1239.81, 856.84, 441.38, 599.95, 1275.11, 1054.99, 2350.20, 1923.67, 1863.53, 981.91, 2099.25, 2160.63, 3768.95]
HOCH_int = [3.866, 2.714, 2.445, 1.987, 1.942, 1.447, 1.219, 1.217, 1.158, 1.003, 0.982, 0.810, 0.698, 0.649, 0.639]
HOCH_comp = [0.00, 0.01, 0.01, 0.01, 0.02, 0.04, 0.03, 0.03, 0.03, 0.04, 0.04, 0.04, 0.05, 0.05, 0.05]
SA_int = [3.192, 2.349, 1.986, 1.832, 1.361, 1.863, 1.428, 1.194, 1.219, 1.233, 1.209, 1.209, 1.194, 1.317, 1.145]
SA_comp = [29.90, 67.47, 91.10, 111.88, 123.28, 121.78, 145.89, 234.00, 262.13, 271.55, 263.73, 319.12, 269.21, 298.71, 347.21]

fig, ax1 = plt.subplots() 
ax1.set_xlabel('K') 
ax1.set_ylabel('Maximum reaction time (hours)') 
ax1.plot(range(1, 16), ILP_int, label='ILP')
ax1.plot(range(1, 16), HOCH_int, label='Hochbaum')
ax1.plot(range(1, 16), SA_int, label='Simulated Annealing')
ax1.tick_params(axis ='y') 
plt.legend()
  
# Adding Twin Axes
ax2 = ax1.twinx()   
ax2.set_ylabel('computation time [s]')
ax2.plot(range(1, 16), ILP_comp, label='ILP', linestyle='dashed')
ax2.plot(range(1, 16), HOCH_comp, label='Hochbaum', linestyle='dashed')
ax2.plot(range(1, 16), SA_comp, label='SA', linestyle='dashed')
ax2.tick_params(axis ='y') 

# show plot
plt.show()
