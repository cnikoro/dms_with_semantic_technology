from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import DiagnosisForm, InsertForm, UpdateForm, VerifyForm
from django.urls import reverse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3
import os
from .fetchData import main
from .insertData import main as insert
from .updateData import main as update
from .deleteData import main as delete
#from sklearn.preprocessing import StandardScaler
#from sklearn.metrics import accuracy_score
#from sklearn.metrics import confusion_matrix
#from sklearn.metrics import precision_score, recall_score
#from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.externals import joblib
from . import settings

def diagnose(request):
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
            if data:
                data = data[0]
            else:
                return render(request, "home.html", {"form": form})
            columns = features
            df = pd.DataFrame(data, index=columns)
            #print(df.shape)
            ddmodel = joblib.load(os.path.join(settings.BASE_DIR, 'DDiag_model_old.pkl'))
            pred = ddmodel.predict_proba(df)
            print(pred)
            predClass = pred.argmax()
            predproba = round((float(pred[0][predClass]) * 100), 2)
            ## Create a plot
            predictions = [pred[0][0], pred[0][1], pred[0][2]]
            labels = ['Non-Diabetic', 'Type 1', 'Type 2']
            idx = np.asarray([i for i in range(len(predictions))])
            #fig = plt.figure(figsize=(2,2))
            #fig = plt.figure()
            fig, ax = plt.subplots(1,1, figsize=(3,2))
            colors = ['aqua', '#FF0CCB', 'yellow']
            #explode=(0.5,0.5)
            #autopct = '%1.1f%%'
            #ax.pie(predictions, labels = labels, frame = True, colors=colors, autopct = autopct, shadow=True, startangle=180, rotatelabels=False)
            ax.barh(labels, predictions, color=colors)
            ax.set_yticks(idx)
            ax.set_xticks([0.0, 0.5, 1.0])
            #ax.set_yticklabels(labels, rotation=45)
            #ax.axis('equal')
            #plt.title('Pie chart showing the prediction statistics', pad=5.5)
            #plt.barh(labels, predictions)
            #plt.xticks(labels, rotation=45)
            #print(dir(plt))
            fig.tight_layout()
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

def insert_view(request):
    data = []
    if request.method == "POST":
        form = InsertForm(request.POST)
        if form.is_valid():
            data.append(form.cleaned_data["pid"])
            data.append(form.cleaned_data["age"])
            data.append(form.cleaned_data["bs"])
            data.append(form.cleaned_data["bp"])
            data.append(form.cleaned_data["pr"])
            data.append(form.cleaned_data["pf"])
            data.append(form.cleaned_data["hbalc"])
            print(data)

            outcome = insert(data, data[0])
            print(outcome)
            #return render(request, "insert.html", {"form": form, "outcome": outcome})
            return redirect(diagnose)
    else:
        form = InsertForm()
    return render(request, "insert.html", {"form": form})

def update_view(request):
    if request.method=="POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data["value"]
            feature = form.cleaned_data["feature"]
            pid = form.cleaned_data["pid"]
            if (str(value)).find(".000") == 1:
                value = int(value)
            data = main("?id", "=", ":{}".format(pid))
            if not data:
                return render(request, "update_with_errors.html", {"form": form})
            outcome = update(feature, value, pid)
            print(outcome)
            #return render(request, "update.html", {"form": form, "outcome": outcome, "data": data})
            return redirect(diagnose)
    else:
        form = UpdateForm()
        print("Hi")
    return render(request, "update.html", {"form": form})

def delete_view(request, patientID):
    """
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid():
            #pid = form.cleaned_data["pid"]
            #ata = main("?id", "=", ":{}".format(pid))
            outcome = delete(pid)
            print(outcome)
            return render(request, "delete.html", {"form":form, "outcome": outcome})
    else:
        form = DeleteForm()
    return render(request, "delete.html", {"form": form})
    """
    _ = delete(patientID)
    return render(request, "delete.html")

def verify_view(request):
    if request.method == "POST":
        form = VerifyForm(request.POST)
        if form.is_valid():
            pid = form.cleaned_data["pid"]
            data = main("?id", "=", ":{}".format(pid))
            print(data)
            if data:
               return render(request, "verify.html", {"form": form, "data": data[0], "pid": pid})
            else:
                return render(request, "verify.html", {"form": form, "pid": pid})
    else:
        form = VerifyForm()
        pid=form["pid"].value()
    return render(request, "verify.html", {"form": form, "pid": pid})

            
