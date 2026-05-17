import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import re

# Redefine the current amplitude function for a series RLC circuit
def current_amplitude(f, R, L, C):
    V_peak = 5  # Peak-to-peak voltage is 5V; V_peak = V_peak-to-peak / 2
    V = V_peak / 2  # Convert to peak voltage
    omega = 2 * np.pi * f  # Angular frequency
    X_L = omega * L  # Inductive reactance
    X_C = 1 / (omega * C)  # Capacitive reactance
    impedance = np.sqrt(R**2 + (X_L - X_C)**2)  # Total impedance
    return V / impedance  # Current amplitude

# Initialize lists to store frequencies and currents
frequencies = []
currents = []

# Directory containing the oscilloscope data files
file_path_pattern = r"C:\Users\Eran\Desktop\day1 AC\*.csv"

# Loop over each CSV file
for file in glob.glob(file_path_pattern):
    print(f"Processing file: {file}")
    # Extract frequency from the file name
    frequency_match = re.search(r"(\d+)Mhz", file)
    if frequency_match:
        frequency = int(frequency_match.group(1)) * 1e6  # Convert MHz to Hz
        print(f"Extracted frequency: {frequency} Hz")
    else:
        print(f"Could not extract frequency from file name: {file}")
        continue
    
    # Load the voltage vs. time data from CSV
    data = pd.read_csv(file, skiprows=10, header=None, usecols=[3, 4], names=["Time", "Voltage"], nrows=1000)
    
    # Calculate the amplitude as the peak-to-peak voltage
    amplitude = np.max(data['Voltage']) - np.min(data['Voltage'])
    
    # Calculate the current using Ohm's Law
    current = amplitude / 1000  # Assume resistance R = 1000 Ω
    
    # Append valid data points
    frequencies.append(frequency)
    currents.append(current)

# Convert lists to numpy arrays
frequencies = np.array(frequencies)
currents = np.array(currents)

# Check if valid data exists
if len(frequencies) == 0 or len(currents) == 0:
    raise ValueError("No valid data points found. Check the data files.")

# Sort the data
sorted_indices = np.argsort(frequencies)
frequencies = frequencies[sorted_indices]
currents = currents[sorted_indices]

# Define initial guesses for R, L, and C
R_initial = 1000  # Resistance in ohms
L_initial = 216e-3  # Inductance in Henry
C_initial = 36e-12  # Capacitance in Farads
initial_guess = [R_initial, L_initial, C_initial]

print(f"Initial guesses:\n"
      f"R = {R_initial:.3e} Ω\n"
      f"L = {L_initial:.3e} H\n"
      f"C = {C_initial:.3e} F")

# Define bounds for the parameters
bounds = ([500, 100e-3, 10e-12], [2000, 500e-3, 100e-12])  # Reasonable ranges for R, L, and C

# Perform the curve fitting with bounds
params, covariance = curve_fit(
    current_amplitude,
    frequencies,
    currents,
    p0=initial_guess,
    bounds=bounds
)

# Extract fitted parameters
R_fit, L_fit, C_fit = params
f_resonance_fit = 1 / (2 * np.pi * np.sqrt(L_fit * C_fit))
print(f"Fitted parameters:\nR = {R_fit:.3e} Ω\nL = {L_fit:.3e} H\nC = {C_fit:.3e} F")
print(f"Fitted resonance frequency: {f_resonance_fit:.3e} Hz")

# Generate data for the fitted curve
frequency_fit = np.linspace(min(frequencies), max(frequencies), 1000)
current_fit = current_amplitude(frequency_fit, R_fit, L_fit, C_fit)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(frequencies, currents, 'o', label='Measured Data', color='blue')  # Scatter plot for data
plt.plot(frequency_fit, current_fit, label='Fitted Curve', color='red')  # Fitted curve
plt.xlabel('Frequency (Hz)')
plt.ylabel('Current (A)')
plt.title('Current vs Frequency with Fitted Resonance Curve')
plt.legend()
plt.grid(True)

# Display fitted parameters on the plot
plt.text(
    min(frequencies),
    max(currents) * 0.8,
    f'R = {R_fit:.3e} Ω\nL = {L_fit:.3e} H\nC = {C_fit:.3e} F',
    fontsize=10,
    bbox=dict(facecolor='white', alpha=0.5)
)

plt.show()
