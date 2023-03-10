import numpy as np
import json
from flask import Flask, request, jsonify, render_template
import pickle
from flask_cors import CORS, cross_origin
app = Flask(__name__)
model = pickle.load(open('hear_disease.pkl', 'rb'))

cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def results():
    data = request.get_json(force=True)

    print(data)

    prediction = model.predict([np.array(list(data.values()))])
    prediction_proba = model.predict_proba([np.array(list(data.values()))])

    print(prediction_proba)
    proba = ''

    if str(prediction[0]) == 0:
        proba = str(prediction_proba[0][1])
    else:
        proba = str(prediction_proba[0][0])

    return {'result': str(prediction[0]), 'proba': proba}


if __name__ == "__main__":
    app.run(debug=True)
