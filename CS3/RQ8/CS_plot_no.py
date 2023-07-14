import matplotlib.pyplot as plt


## NO
ILP_int = [2.333, 1.477, 1.251, 0.853, 0.836, 0.555, 0.484, 0.393, 0.287, 0.285, 0.267, 0.258, 0.243, 0.231, 0.207]
ILP_comp = [2.65, 128.77, 81.52, 80.44, 79.14, 56.58, 55.04, 67.97, 64.15, 63.49, 40.43, 55.81, 47.28, 70.52, 54.29]
HOCH_int = [3.789, 1.995, 1.370, 1.261, 1.005, 0.770, 0.520, 0.500, 0.433, 0.426, 0.425, 0.369, 0.311, 0.260, 0.258]
HOCH_comp = [0.01, 0.01, 0.01, 0.01, 0.01, 0.02, 0.01, 0.02, 0.02, 0.02, 0.02, 0.02, 0.01, 0.02, 0.02]
SA_int = [2.33, 1.501, 1.326, 0.921, 0.853, 0.855, 0.853, 0.847, 1.326, 0.847, 0.583, 0.457, 0.500, 0.847, 0.905]
SA_comp = [3.62, 10.92, 16.11, 23.08, 29.44, 35.98, 42.45, 48.22, 48.78, 34.56, 39.07, 41.33, 44.81, 48.99, 51.06]



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
