
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("placement_model.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        iq = float(request.form['IQ'])
        prev = float(request.form['Prev_Sem_Result'])
        cgpa = float(request.form['CGPA'])
        ap = int(request.form['Academic_Performance'])
        intern = 1 if request.form['Internship_Experience'] == "Yes" else 0
        ecs = int(request.form['Extra_Curricular_Score'])
        comm = int(request.form['Communication_Skills'])
        proj = int(request.form['Projects_Completed'])

        features = np.array([[iq, prev, cgpa, ap, intern, ecs, comm, proj]])
        pred = model.predict(features)[0]
        result = "Yes" if pred == 1 else "No"
        return render_template('index.html', prediction_text=f'Placement Prediction: {result}')
    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        data = request.get_json()
        features = np.array([
            data['IQ'],
            data['Prev_Sem_Result'],
            data['CGPA'],
            data['Academic_Performance'],
            1 if data['Internship_Experience'] == "Yes" else 0,
            data['Extra_Curricular_Score'],
            data['Communication_Skills'],
            data['Projects_Completed']
        ]).reshape(1, -1)
        prediction = model.predict(features)[0]
        return jsonify({'placement': "Yes" if prediction == 1 else "No"})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
