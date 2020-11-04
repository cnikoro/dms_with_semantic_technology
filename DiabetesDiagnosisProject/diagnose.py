
import pandas as pd
import numpy as np
from sklearn.externals import joblib
#import joblib
from fetchData import main
import os

FEATURES = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
            "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
data = main("?id", "=", ":1")
data = data[0]
columns = FEATURES

df = pd.DataFrame(data, index=columns)
print(df.shape)
ddmodel = joblib.load('diabetesModel.pkl')
pred = ddmodel.predict_proba(df)
#print(pred)
predClass = pred.argmax()
predproba = round((float(pred[0][predClass]) * 100), 2)
print(predClass, predproba)
