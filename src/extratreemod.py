import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Load the dataset
data = pd.read_csv('waterbodies_dataset.csv')

# Check for missing values
print(data.isnull().sum())

# Encode categorical variable (Bioremediating Organism)
label_encoder = LabelEncoder()
data['Bioremediating Organism'] = label_encoder.fit_transform(data['Bioremediating Organism'])

# Define features and target variable 
X = data[['Temperature (°C)', 'pH', 'Dissolved O2 (mg/L)', 'BOD (mg/L)','Conductivity (µS/cm)', 'Salinity (ppt)','Nitrate-N Concentration (mg/L)']]
y = data['Bioremediating Organism']

# Scale features 
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the dataset into training and testing sets 
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize and train the model 
et_model = ExtraTreesClassifier(n_estimators=100, bootstrap=True, random_state=42)
et_model.fit(X_train, y_train)

# Make predictions on the test set 
y_pred_et = et_model.predict(X_test)

# Evaluate the model 
print("Accuracy (Extra Trees):", accuracy_score(y_test, y_pred_et))
print(classification_report(y_test, y_pred_et))

# Save the trained model and label encoder 
if not os.path.exists('models'):
    os.makedirs('models')
joblib.dump(et_model, 'models/et_model.pkl')
joblib.dump(label_encoder, 'models/label_encoder.pkl')
