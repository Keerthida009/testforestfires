import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd  # Corrected pandas alias
from sklearn.preprocessing import StandardScaler

application = Flask(__name__)
app = application

try:
    ridge_model = pickle.load(open('models/ridge.pkl', 'rb'))
    standard_scaler = pickle.load(open('models/scaler.pkl', 'rb'))
except Exception as e:
    print(f"Error loading models: {e}")
    ridge_model = None
    standard_scaler = None

@app.route("/")
def index():
    return render_template('home.html')  # Render home.html directly

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == "POST":
        def safe_float(value):
            try:
                return float(value) if value not in [None, "", " "] else 0.0
            except ValueError:
                return 0.0

        try:
            Temperature = safe_float(request.form.get('Temperature'))
            RH = safe_float(request.form.get('RH'))
            Ws = safe_float(request.form.get('Ws'))
            Rain = safe_float(request.form.get('Rain'))
            FFMC = safe_float(request.form.get('FFMC'))
            DMC = safe_float(request.form.get('DMC'))
            ISI = safe_float(request.form.get('ISI'))
            Classes = safe_float(request.form.get('Classes'))
            Region = safe_float(request.form.get('Region'))

            new_data = np.array([[Temperature, RH, Ws, Rain, FFMC, DMC, ISI, Classes, Region]])
            new_data_scaled = standard_scaler.transform(new_data)
            result = ridge_model.predict(new_data_scaled)[0]

            if result < 5:
                risk_level = "Low Fire Risk 🟢"
            elif 5 <= result < 10:
                risk_level = "Moderate Fire Risk 🟡"
            elif 10 <= result < 20:
                risk_level = "High Fire Risk 🟠"
            else:
                risk_level = "Extreme Fire Risk 🔴"

            return render_template('home.html', results=result, risk_level=risk_level)

        except Exception as e:
            print(f"Prediction error: {e}")
            return render_template('home.html', error="An error occurred during prediction.")

    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)  # debug=False for production!
