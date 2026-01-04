from flask import Flask, request, jsonify
import os
import joblib
import numpy as np
import logging
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token,current_user,jwt_required,get_jwt_identity


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

modelfolder = "/app/model/"
modelname = "winemodel"
version = "v1" 

app = Flask(__name__)
app.config["JWT_SECRET_KEY"]="FVKEFNVKLEFLVJLFELVOEJVOEI4R802874029RJKFNRKJFR"
jwt=JWTManager(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # /app/api
modelPath = os.path.join(BASE_DIR, "..", modelfolder, f"{modelname}_{version}.pkl")
modelPath = os.path.abspath(modelPath)

logging.info(f"Loading model from: {modelPath}")
model = joblib.load(modelPath)
logging.info("Model Loaded Successfully")


featurelist = [
    'fixed acidity','volatile acidity','citric acid','residual sugar','chlorides',
    'free sulfur dioxide','total sulfur dioxide','density','pH','sulphates','alcohol'
]

def input_check(inputdata):
    inputarray = []
    for feature in featurelist:
        value = inputdata.get(feature)
        if value is None:
            logging.error(f"Missing input: {feature}")
            return f"Missing feature: {feature}"
        inputarray.append(value)
    return np.array(inputarray)


@app.route("/login",methods=["POST"])
def login():
    data=dict(request.get_json())
    username=data.get("username")
    password=data.get("password")
    print("__________________________________")

    if not username or not password:
        return jsonify({"success": False, "message": "Invaild username or password"})
    
    access_token=create_access_token(identity=username)
    return jsonify({"success": True, "message": access_token})
    



@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"success": True, "message": "Server is Running"})

@app.route("/predict", methods=["POST"])
@jwt_required()
def model_predict():
    current_user = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No Input Data"})

    sani_input = input_check(data)

    if isinstance(sani_input, np.ndarray):
        prediction = model.predict([sani_input])
        return jsonify({
            "success": True,
            "message": "Prediction successful",
            "data": {"prediction": str(prediction)}
        })
    else:
        return jsonify({"success": False, "message": sani_input})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)




