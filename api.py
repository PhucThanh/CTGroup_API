import numpy as np
import pandas as pd
import random
import pip
from flask import Flask,render_template,request, redirect
from flask_restful import Resource, Api, reqparse

try:
  pip.main(['install', 'apyori'])
except ImportError:
  print('apyori was installed')
from apyori import apriori


app = Flask(__name__)
api = Api(app)

dataset = pd.read_csv('./Results.csv',sep=',')
dataset['items_buy']=(dataset['items_base']).str.split()
uni=[]
for i in dataset['items_buy']:
    for k in i:
        if k not in uni: uni.append(k)
uni=np.sort(uni)
res = {}
for i in range(0, len(uni)):
    res[i]=uni[i]


def Suggest1(a):
    X=[]
    Y=[]
    a=list(np.sort(a))
    for i in range(1, len(dataset['items_buy'])):
        b=list(np.sort(dataset['items_buy'][i]))
        if a==b: 
          X.append(dataset['items_add'][i])
          Y.append(dataset['confidence'][i])
    if len(a)>=2:
        for i in range(0, len(a)):
          for j in range(0, len(dataset['items_buy'])):
            b=dataset['items_buy'][j]
            if a[i] in b: 
              X.append(dataset['items_add'][j])
              Y.append(dataset['confidence'][j])
    for i in range(0, len(a)):
      while a[i] in X: 
        X.remove(a[i])
        Y.remove(Y[i])
    Z = [x for _,x in sorted(zip(Y,X))]
    M = np.unique(Z, return_index=True)[1]
    return [(Z[i],round(Y[i],2)) for i in sorted(M, reverse=True)]

@app.route('/')
def home():
    return render_template('index.html',res=res)
@app.route('/submit',methods=['POST'])
def submit():
    req = request.form
    c=[]
    for i,n in req.items():
        c.append(res[int(i)])
    suggest=Suggest1(c)
    d = dict(enumerate(suggest, 1))
    print(suggest)
    return render_template('result.html',res=suggest)
if __name__=='__main__':
    app.run(debug=True)
