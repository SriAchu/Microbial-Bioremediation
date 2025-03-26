import pandas as pd

# Load your dataset
df = pd.read_csv('waterbodies_dataset.csv')  # Replace 'your_dataset.csv' with the actual dataset file path

# Check the target column (microorganism) distribution
print("Class Distribution:\n")
print(df['Bioremediating Organism'].value_counts())  # Replace 'target_column' with your actual label column name