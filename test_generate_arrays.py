# TEST FUNCTION --> JUST CREATE LIST OF ARRAYS

import numpy as np

min_voltage = 10
max_voltage = 10
data_points = 10
voltages = np.linspace(min_voltage, max_voltage, num=data_points)
currents = np.zeros_like(voltages)
current_stds = np.zeros_like(voltages)
print("Init Voltages:",voltages)
print("Init Currents:",currents)
print("Init stds Currents:",current_stds)
