import tkinter as tk
from tkinter import messagebox
import joblib
import numpy as np

# Load the trained model and label encoder
model = joblib.load('models/et_model.pkl')
label_encoder = joblib.load('models/label_encoder.pkl')

# Microbial remediation mapping
remediation_map = {
    "Ideonella sakaiensis": ["Plastic materials on the water body"],
    "Pseudomonas putida": [
        "Organic waste such as Slug, Feaces, food, wet waste",
        "Sediments deep down.. black/gray/brown, metal sheen"
    ],
    "Pseudomonas aeruginosa": [
        "Organic waste such as Slug, Feaces, food, wet waste",
        "Oily films, discoloration, and algal overgrowth"
    ],
    "Bacillus cereus": ["Sediments deep down.. black/gray/brown, metal sheen"],
    "Acinetobacter baumannii": ["Sediments deep down.. black/gray/brown, metal sheen"],
    "Alcaligenes eutrophus": [
        "Plastic materials on the water body",
        "Organic waste such as Slug, Feaces, food, wet waste",
        "Sediments deep down.. black/gray/brown, metal sheen",
        "Oily films, discoloration, and algal overgrowth"
    ]
}

# Helper to determine remediation capability
# Helper to determine which impurities the organism can remediate
def remediation_check(predicted_class, effects_selected):
    messages = []

    if "Plastic materials on the water body" in effects_selected:
        if predicted_class == "Ideonella sakaiensis":
            messages.append("The predicted microbe will be able to do plastic remediation.\n")
        else:
            messages.append("The predicted microbe  will not be able to do plastic remediation.\n")

    if "Organic waste such as Slug, Feaces, food, wet waste" in effects_selected:
        if predicted_class in ["Pseudomonas putida", "Pseudomonas aeruginosa"]:
            messages.append("The predicted microbe will be able to do organic remediation.\n")
        else:
            messages.append("The predicted microbe  will not be able to do organic remediation.\n")

    if "Sediments deep down.. black/gray/brown, metal sheen" in effects_selected:
        if predicted_class in ["Pseudomonas putida", "Bacillus cereus", "Acinetobacter baumannii"]:
            messages.append("The predicted microbe will be able to do heavy metal remediation.\n")
        else:
            messages.append("The predicted microbe  will not be able to do heavy metal remediation.\n")

    if "Oily films, discoloration, and algal overgrowth" in effects_selected:
        if predicted_class == "Pseudomonas aeruginosa":
            messages.append("The predicted microbe will be able to do pesticide remediation.")
        else:
            messages.append("The predicted microbe  will not be able to do pesticide remediation.")

    return messages



def predict():
    # Get user input from sliders
    temperature = temperature_scale.get()
    ph = ph_scale.get()
    dissolved_o2 = do_scale.get()
    bod = bod_scale.get()
    conductivity = cond_scale.get()
    salinity = salinity_scale.get()
    nitrate_n = nitrate_scale.get()

    # Prepare input data for prediction
    raw_input_data = np.array([temperature, ph, dissolved_o2, bod, conductivity, salinity, nitrate_n])
    input_data = preprocess_input(raw_input_data)

    # Debugging: Print input data
    print("Raw Input Data:", raw_input_data)
    print("Normalized Input Data:", input_data)

    # Make prediction
    prediction = model.predict(input_data)

    # Debugging: Print raw prediction (class index)
    print("Raw Prediction (class index):", prediction)

    # Transform to class name
    predicted_class = label_encoder.inverse_transform(prediction)[0]

    # Debugging: Print predicted class
    print("Predicted Class:", predicted_class)

    # Check for selected effects
    effects_selected = []
    if var_plastic.get():
        effects_selected.append("Plastic materials on the water body")
    if var_organic.get():
        effects_selected.append("Organic waste such as Slug, Feaces, food, wet waste")
    if var_hvmetals.get():
        effects_selected.append("Sediments deep down.. black/gray/brown, metal sheen")
    if var_pesticides.get():
        effects_selected.append("Oily films, discoloration, and algal overgrowth")

    # Determine remediation capability
    remediation_messages = remediation_check(predicted_class, effects_selected)

    remediation_message = f"The predicted microbe that can survive in the specified environment is: {predicted_class}.\n\n"
    remediation_message += "\n".join(remediation_messages)

    # Display result
    messagebox.showinfo("Prediction Result", remediation_message)

# Preprocess input function remains unchanged
def preprocess_input(data):
    """
    Preprocess the input data (e.g., scaling or normalization).
    Adjust this function to match your training data preprocessing.
    """
    # Example: Normalize data based on training ranges
    ranges = {
        'temperature': (20, 30),
        'ph': (6.0, 9.0),
        'dissolved_o2': (5, 14),
        'bod': (1, 20),
        'conductivity': (50, 1500),
        'salinity': (0, 5),
        'nitrate_n': (0, 60)
    }

    normalized_data = []
    for i, key in enumerate(ranges):
        min_val, max_val = ranges[key]
        normalized_data.append((data[i] - min_val) / (max_val - min_val))

    return np.array([normalized_data])

# Set up the main application window
root = tk.Tk()
root.title("Microorganism Remediation Predictor")
root.configure(bg="#f0f8ff")  # Light blue background for the root window

# Add 'Parameters' heading
tk.Label(root, text="Parameters", font=("Arial", 12, "bold"), bg="#87cefa", fg="white").grid(row=0, columnspan=2, pady=5)

# Create input labels and sliders with vibrant colors
label_bg = "#f0f8ff"  # Background for labels
slider_bg = "#e0ffff"  # Slider background
trough_color = "#87cefa"  # Slider trough color

tk.Label(root, text="Temperature (\u00b0C):", bg=label_bg).grid(row=1, sticky="w")
temperature_scale = tk.Scale(root, from_=20, to=30, orient=tk.HORIZONTAL, bg=slider_bg, troughcolor=trough_color)
temperature_scale.set(25)
temperature_scale.grid(row=1, column=1)

tk.Label(root, text="pH:", bg=label_bg).grid(row=2, sticky="w")
ph_scale = tk.Scale(root, from_=6.0, to=9.0, resolution=0.1, orient=tk.HORIZONTAL, bg=slider_bg, troughcolor=trough_color)
ph_scale.set(7.0)
ph_scale.grid(row=2, column=1)

tk.Label(root, text="Dissolved O2 (mg/L):", bg=label_bg).grid(row=3, sticky="w")
do_scale = tk.Scale(root, from_=5, to=14, orient=tk.HORIZONTAL, bg=slider_bg, troughcolor=trough_color)
do_scale.set(8)
do_scale.grid(row=3, column=1)

tk.Label(root, text="BOD (mg/L):", bg=label_bg).grid(row=4, sticky="w")
bod_scale = tk.Scale(root, from_=1, to=20, orient=tk.HORIZONTAL, bg=slider_bg, troughcolor=trough_color)
bod_scale.set(5)
bod_scale.grid(row=4, column=1)

tk.Label(root, text="Conductivity (\u00b5S/cm):", bg=label_bg).grid(row=5, sticky="w")
cond_scale = tk.Scale(root, from_=50, to=1500, orient=tk.HORIZONTAL, bg=slider_bg, troughcolor=trough_color)
cond_scale.set(500)
cond_scale.grid(row=5, column=1)

tk.Label(root, text="Salinity (ppt):", bg=label_bg).grid(row=6, sticky="w")
salinity_scale = tk.Scale(root, from_=0, to=5, resolution=0.1, orient=tk.HORIZONTAL, bg=slider_bg, troughcolor=trough_color)
salinity_scale.set(2)
salinity_scale.grid(row=6, column=1)

tk.Label(root, text="Nitrate-N Concentration (mg/L):", bg=label_bg).grid(row=7, sticky="w")
nitrate_scale = tk.Scale(root, from_=0, to=60, orient=tk.HORIZONTAL, bg=slider_bg, troughcolor=trough_color)
nitrate_scale.set(10)
nitrate_scale.grid(row=7, column=1)

# Add 'Physical Changes Seen' heading
tk.Label(root, text="Physical Changes Seen", font=("Arial", 12, "bold"), bg="#87cefa", fg="white").grid(row=8, columnspan=2, pady=5)

# Create checkboxes for physical effects
checkbox_bg = "#f0f8ff"  # Checkbox background
var_plastic = tk.BooleanVar()
var_organic = tk.BooleanVar()
var_hvmetals = tk.BooleanVar()
var_pesticides = tk.BooleanVar()

tk.Checkbutton(root, text='Plastic materials on the water body', variable=var_plastic, bg=checkbox_bg).grid(row=9, columnspan=2, sticky='w')
tk.Checkbutton(root, text='Organic waste such as Slug, Feaces, food, wet waste', variable=var_organic, bg=checkbox_bg).grid(row=10, columnspan=2, sticky='w')
tk.Checkbutton(root, text='Sediments deep down.. black/gray/brown, metal sheen', variable=var_hvmetals, bg=checkbox_bg).grid(row=11, columnspan=2, sticky='w')
tk.Checkbutton(root, text='Oily films, discoloration, and algal overgrowth', variable=var_pesticides, bg=checkbox_bg).grid(row=12, columnspan=2, sticky='w')

# Create a predict button with vibrant color
predict_button = tk.Button(root, text="Predict", command=predict, bg="#32cd32", fg="white", font=("Arial", 10, "bold"), activebackground="#228b22")
predict_button.grid(row=13, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()
