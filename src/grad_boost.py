import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
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
X = data[['Temperature (°C)', 'pH', 'Dissolved O2 (mg/L)', 'BOD (mg/L)', 'Conductivity (µS/cm)', 'Salinity (ppt)','Nitrate-N Concentration (mg/L)']]

y = data['Bioremediating Organism']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize and train the model
gb_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
gb_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred_gb = gb_model.predict(X_test)

# Evaluate the model
print("Accuracy (Gradient Boosting):", accuracy_score(y_test, y_pred_gb))
print(classification_report(y_test, y_pred_gb))

# Save the trained model and label encoder
if not os.path.exists('models'):
    os.makedirs('models')
joblib.dump(gb_model, 'models/gb_model.pkl')
joblib.dump(label_encoder, 'models/label_encoder.pkl')