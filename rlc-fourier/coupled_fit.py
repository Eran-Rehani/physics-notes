import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Directory containing CSV files
data_folder = "C:/Users/Eran/Desktop/Coupled Circuit"  
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

# Storage for frequencies and amplitudes
frequencies = []
amplitudes = []

# Loop through each CSV file
for file in csv_files:
    # Extract the frequency from the file name
    # Assuming file name format like "0.5Mhz coupled circuit.csv"
    try:
        frequency_mhz = float(file.split("Mhz")[0])  # Extract part before "Mhz" and convert to float
    except ValueError:
        print(f"Error parsing frequency from file name: {file}")
        continue
    frequency_hz = frequency_mhz * 1e6  # Convert to Hz
    frequencies.append(frequency_hz)
    
    # Load the voltage vs time data
    data = pd.read_csv(os.path.join(data_folder, file))
    time = data.iloc[:, 3].to_numpy()  # Assuming time is in the first column
    voltage = data.iloc[:, 10].to_numpy()  # Assuming voltage is in the second column
    
    # Calculate the amplitude
    from scipy.ndimage import gaussian_filter1d
    smoothed_voltage = gaussian_filter1d(voltage, sigma=5)
    amplitude = np.max(np.abs(smoothed_voltage))# Peak amplitude
    #amplitude = np.sqrt(np.mean(voltage**2))
    amplitudes.append(amplitude)

# Sort data by frequency for better visualization
sorted_indices = np.argsort(frequencies)
frequencies = np.array(frequencies)[sorted_indices]
amplitudes = np.array(amplitudes)[sorted_indices]

# Plot the amplitude vs frequency
plt.figure(figsize=(10, 6))
plt.plot(frequencies / 1e6, amplitudes, 'o-', label='Amplitude vs Frequency')  # Convert frequency to MHz
plt.title('Resonance Curve of Coupled RLC System')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Amplitude (V)')
plt.grid()
plt.legend()
plt.show()

# Plot Voltage vs Time for Inspection
plt.figure(figsize=(10, 6))
plt.plot(time, voltage, label=f'Voltage for {file}')
plt.title(f'Voltage vs Time - {file}')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid()
plt.legend()
plt.show()
