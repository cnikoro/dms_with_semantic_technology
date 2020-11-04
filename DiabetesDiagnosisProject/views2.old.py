from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import DiagnosisForm
from django.urls import reverse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3
import os
from .fetchData import main
#from sklearn.preprocessing import StandardScaler
#from sklearn.metrics import accuracy_score
#from sklearn.metrics import confusion_matrix
#from sklearn.metrics import precision_score, recall_score
#from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.externals import joblib
from . import settings

"""
def test(request):
    return HttpResponse("<h1>This is only a test</h1>")
"""

def test(request):
    data=[]
    if request.method == 'POST':
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            # process the form with our model
            patientID=(form.cleaned_data['patientID'])
            """
            glu=form.cleaned_data["glu"]
            bp=form.cleaned_data["bp"]
            st=form.cleaned_data["st"]
            isl=form.cleaned_data["isl"]
            bmi=form.cleaned_data["bmi"]
            dpf=form.cleaned_data["dpf"]
            age=form.cleaned_data["age"]
            data = np.array([[no_preg,glu,bp,st,isl,bmi,dpf,age]])
            data = data.astype('float32')
            """
            features = ['Age', 'BS Fast', 'BS pp', 'Plasma R', 'Plasma F', 'HbAlc']
            data = main("?id", "=", ":{}".format(patientID))
            data = data[0]
            columns = features
            df = pd.DataFrame(data, index=columns)
            #print(df.shape)
            ddmodel = joblib.load(os.path.join(settings.BASE_DIR, 'DDiag_model.pkl'))
            pred = ddmodel.predict_proba(df)
            print(pred)
            predClass = pred.argmax()
            predproba = round((float(pred[0][predClass]) * 100), 2)
            ## Create a plot
            predictions = [pred[0][0], pred[0][1], pred[0][2]]
            labels = ('Non-Diabetic', 'Type 1', 'Type 2')
            #fig = plt.figure(figsize=(2,2))
            fig, ax = plt.subplots(1,1, figsize=(3,2))
            colors = ['aqua', '#FF0CCB', 'yellow']
            #explode=(0.5,0.5)
            autopct = '%1.1f%%'
            ax.pie(predictions, labels = labels, frame = True, colors=colors, autopct = autopct, shadow=True, startangle=180, rotatelabels=False)
            ax.axis('equal')
            #plt.title('Pie chart showing the prediction statistics', pad=5.5)
            graph = mpld3.fig_to_html(fig)
            display = 0
            #plt.savefig('static/graph.png')
            #path = os.path.abspath('../templates')
            #os.system('touch {}/graph.html'.format(path))
            #f = open(path+'/graph.html', 'w')
            with open(os.path.join(settings.BASE_DIR, 'templates/graph.html'), 'w') as f:
                f.write(graph)
            #f.close()
            print(predproba)
            return render(request, "home.html", {'predClass': predClass, 'probability': predproba, 'form': form, 'data': data, 'display': display, 'graph': graph})
    else:
        form = DiagnosisForm()
    return render(request, "home.html", {'form':form, 'data': data})
