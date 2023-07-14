import matplotlib.pyplot as plt 

## maak mooie prints van de resultaten van de simulatie

ILP_1 = [5.1293029, 2.9120733, 2.0717999, 1.5851943, 1.2689512, 1.2557916, 0.92028042, 0.75557173, 0.70310402, 0.62287631, 0.0]
ILP_1_clocks = [0.08, 0.14, 0.13, 0.18, 0.2, 0.17, 0.25, 0.09, 0.08, 0.11, 0.04]
ILP_2 = [6.6016028, 3.7479462, 2.6664833, 2.0402037, 1.6331872, 1.6162503, 1.184435, 0.9724488, 0.90492091, 0.80166488, 0.0]
ILP_2_clocks = [0.07, 0.15, 0.11, 0.17, 0.45, 0.19, 0.35, 0.1, 0.1, 0.11, 0.04]

HOCH_1 = [9.84, 4.93, 2.55, 2.13, 1.9, 1.26, 0.92, 0.76, 0.7, 0.62, 0]
HOCH_1_clocks = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
HOCH_2 = [12.67, 6.34, 3.28, 2.74, 2.45, 1.62, 1.18, 0.97, 0.9, 0.8, 0]
HOCH_2_clocks = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

SA_1 = [5.13, 2.91, 2.07, 1.71, 1.27, 1.26, 0.92, 1.26, 0.7, 0.7, 0]
SA_1_clocks = [0.03, 0.07, 0.08, 0.1, 0.12, 0.15, 0.17, 0.19, 0.22, 0.23, 0.25]
SA_2 = [6.6, 3.75, 2.67, 2.2, 1.63, 1.62, 1.18, 0.97, 0.97, 0.9, 0]
SA_2_clocks = [0.02, 0.04, 0.05, 0.07, 0.1, 0.11, 0.13, 0.13, 0.15, 0.17, 0.18]

# asset type 1

fig, ax1 = plt.subplots() 
ax1.set_xlabel('K') 
ax1.set_ylabel('Maximum reaction time (hours)') 
ax1.plot(range(1, 12), ILP_1, label='ILP')
ax1.plot(range(1, 12), HOCH_1, label='Hochbaum')
ax1.plot(range(1, 12), SA_1, label='SA')
ax1.tick_params(axis ='y') 
plt.legend()
  
# Adding Twin Axes
ax2 = ax1.twinx()   
ax2.set_ylabel('computation time [s]')
ax2.plot(range(1, 12), ILP_1_clocks, label='ILP', linestyle='dashed')
ax2.plot(range(1, 12), HOCH_1_clocks, label='Hochbaum', linestyle='dashed')
ax2.plot(range(1, 12), SA_1_clocks, label='SA', linestyle='dashed')
ax2.tick_params(axis ='y') 

# show plot
plt.show()

# asset type 2

fig, ax1 = plt.subplots() 
ax1.set_xlabel('K') 
ax1.set_ylabel('Maximum reaction time (hours)') 
ax1.plot(range(1, 12), ILP_2, label='ILP')
ax1.plot(range(1, 12), HOCH_2, label='Hochbaum')
ax1.plot(range(1, 12), SA_2, label='SA')
ax1.tick_params(axis ='y') 
plt.legend()
  
# Adding Twin Axes
ax2 = ax1.twinx()   
ax2.set_ylabel('computation time [s]')
ax2.plot(range(1, 12), ILP_2_clocks, label='ILP', linestyle='dashed')
ax2.plot(range(1, 12), HOCH_2_clocks, label='Hochbaum', linestyle='dashed')
ax2.plot(range(1, 12), SA_2_clocks, label='SA', linestyle='dashed')
ax2.tick_params(axis ='y') 

# show plot
plt.show()