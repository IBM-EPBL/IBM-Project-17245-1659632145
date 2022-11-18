import requests
import json
import pandas as pd
import pickle
import numpy as np
from flask import Flask, request, render_template

app = Flask (__name__,template_folder='template') # initializing a flask app
model = pickle.load(open('CKD1.pkl', 'rb')) #loading the model

@app.route('/')# route to display the home page
def home():
    return render_template('index.html')
@app.route('/Prediction')
def prediction (): # route to display prediction page
    return render_template('web.html')
@app.route("/Home")
def my_home():
    return render_template('index.html')

@app.route("/result")
def result():
        return render_template('report.html')

@app.route('/predict', methods=['POST'])
def predict():
    burea=float(request.form.get("burea"))
    bglucose=float(request.form.get("bglucose"))
    input_features=[float(x) for x in request.form.values()]
    print(burea)
    print(bglucose)
    print(input_features)
    features_value = [np.array(input_features)]
    features_name = ['red_blood_cells','pus_cell','blood glucose random','blood_urea','pedal_edema','anemia','diabetesmellitus','coronary_artery_disease']
    df = pd.DataFrame (features_value, columns=features_name, dtype= float)

    API_KEY = "hCgkjwBiCxoEsdog_EtgqD5xYXmz00Er5d9wn_V9Rdxw"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    header = {'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + mltoken}
    payload_scoring = {"input_data": [{"field": [['red_blood_cells', 'pus_cell', 'blood glucose random', 'blood_urea',
                                                'pedal_edema', 'anemia', 'diabetesmellitus', 'coronary_artery_disease']], 
                                                "values": df}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/1f458eb5-a5bd-4637-9457-51fcaea1b16b/predictions?version=2022-11-17', json=payload_scoring,
                                    headers={'Authorization': 'Bearer ' + mltoken})
    predictions = response_scoring.json()
    pred = predictions['predictions'][0]['values'][0][0]

    if pred==1:
        return render_template('report.html', prediction_text='Oops! You have Chronic Kidney Disease.')
    else:
        return render_template('report.html', prediction_text='You do not have Chronic Kidney Disease.')

if __name__=='__main__':
    app.run(debug=True,port=5001)
