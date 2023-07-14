import matplotlib.pyplot as plt



## DK
ILP_int = [0.779, 0.542, 0.378, 0.290, 0.226, 0.174, 0.172, 0.128, 0.107, 0.106, 0.097, 0.073, 0.072, 0.068, 0.060]
ILP_comp = [1.27, 19.22, 22.51, 15.43, 16.26, 13.92, 16.87, 27.39, 16.41, 25.73, 18.29, 14.46, 34.55, 19.18, 23.34]
HOCH_int = [1.007, 0.699, 0.527, 0.392, 0.273, 0.245, 0.196, 0.176, 0.149, 0.106, 0.097, 0.092, 0.086, 0.073, 0.065]
HOCH_comp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
SA_int = [0.779, 0.543, 0.378, 0.321, 0.249, 0.400, 0.237, 0.177, 0.224, 0.240, 0.224, 0.224, 0.224, 0.128, 0.239]
SA_comp = [1.18, 2.26, 5.12, 7.85, 9.54, 11.94, 13.06, 15.40, 16.13, 18.14, 19.26, 22.90, 22.90, 16.61, 15.75]

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


