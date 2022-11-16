import pandas as pd
from flask import Flask, request, render_template
import pickle
import numpy as np

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
#reading the inputs given by the user
    burea=float(request.form.get("burea"))
    bglucose=float(request.form.get("bglucose"))
    input_features=[float(x) for x in request.form.values()]
    print(burea)
    print(bglucose)
    print(input_features)
    features_value = [np.array(input_features)]
    features_name = ['red_blood_cells','pus_cell','blood glucose random','blood_urea','pedal_edema','anemia','diabetesmellitus','coronary_artery_disease']
    df = pd.DataFrame (features_value, columns=features_name, dtype= float)
    output = model.predict(df) # predictions using the loaded model file
# showing the prediction results in a UI# showing the prediction results in a UI
    return render_template('report.html', prediction_text=output)
if __name__=='__main__':
    app.run(debug=True,port=8000) # running the app
