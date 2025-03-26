import pandas as pd
import numpy as np

# Constants
num_samples = 10000  # Increased sample size
temperature_range = (20, 30)   # Updated temperature range (realistic for selected organisms)
pH_range = (6.0, 9.0)          # Typical pH range for freshwater
dissolved_o2_range = (5, 14)    # mg/L (reasonable range for dissolved oxygen)
bod_range = (1, 20)              # mg/L (BOD levels)
conductivity_range = (50, 1500)  # µS/cm (realistic conductivity range for freshwater)
salinity_range = (0, 5)          # ppt (realistic salinity range for freshwater)
nitrate_n_range = (0, 60)        # mg/L (Nitrate-N concentration)

# Define organisms and their preferred environmental conditions
organism_conditions = {
    "Ideonella sakaiensis": {"temp": (20, 30), "pH": (6.5, 7.5), "dO2": (8, 14), "BOD": (2, 10), "conductivity": (200, 600), "salinity": (4, 5), "nitrate_n": (0, 20)},
    "Pseudomonas putida": {"temp": (20, 25), "pH": (6.0, 7.5), "dO2": (7, 12), "BOD": (1, 5), "conductivity": (100, 400), "salinity": (3.5, 4), "nitrate_n": (0, 15)},
    "Pseudomonas aeruginosa": {"temp": (25, 30), "pH": (7.0, 9.0), "dO2": (5, 10), "BOD": (4, 15), "conductivity": (300, 800), "salinity": (0, 2), "nitrate_n": (10, 30)},
    "Bacillus cereus": {"temp": (20, 25), "pH": (6.5, 8.0), "dO2": (6, 11), "BOD": (3, 10), "conductivity": (150, 500), "salinity": (2, 3), "nitrate_n": (5, 25)},
    "Acinetobacter baumannii": {"temp": (20, 28), "pH": (6.5, 7.5), "dO2": (8, 14), "BOD": (2, 8), "conductivity": (400, 1000), "salinity": (0, 2.5), "nitrate_n": (15, 40)},
    "Alcaligenes eutrophus": {"temp": (20, 30), "pH": (7.0, 9.0), "dO2": (5, 12), "BOD": (1, 15), "conductivity": (100, 700), "salinity": (0, 1), "nitrate_n": (0, 10)}
}

# Generate data with conditions
data = []

for _ in range(num_samples):
    # Randomly select an organism based on its conditions
    organism = np.random.choice(list(organism_conditions.keys()))
    
    # Get the preferred conditions for the selected organism
    conditions = organism_conditions[organism]
    
    # Generate values within the specified ranges for the selected organism
    temperature = round(np.random.uniform(*conditions["temp"]), 2)
    ph = round(np.random.uniform(*conditions["pH"]), 2)
    dissolved_o2 = round(np.random.uniform(*conditions["dO2"]), 2)
    bod = round(np.random.uniform(*conditions["BOD"]), 2)
    conductivity = round(np.random.uniform(*conditions["conductivity"]), 2)
    salinity = round(np.random.uniform(*conditions["salinity"]), 2)

    # Introduce a correlation between Nitrate-N and other parameters
    if bod > 10:
        nitrate_n = round(np.random.uniform(15, conditions["nitrate_n"][1]), 2)   # Higher nitrate due to high BOD
    else:
        nitrate_n = round(np.random.uniform(*conditions["nitrate_n"]), 2)         # Normal nitrate levels

    data.append([temperature, ph, dissolved_o2, bod, conductivity, salinity, nitrate_n, organism])

# Create DataFrame
df = pd.DataFrame(data,
                  columns=['Temperature (°C)', 'pH', 'Dissolved O2 (mg/L)', 'BOD (mg/L)', 'Conductivity (µS/cm)', 'Salinity (ppt)', 'Nitrate-N Concentration (mg/L)', 'Bioremediating Organism'])

# Save to CSV
df.to_csv('waterbodies_dataset.csv', index=False)
