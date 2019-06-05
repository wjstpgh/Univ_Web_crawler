import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

@app.route('/')

def home():
    return render_template('home.html')

dir=os.path.dirname(os.path.abspath(__file__))
##path that the result file will be stored

##req=requests.get('https://www.naver.com/')
##get sourse
req=requests.form['site']
con=requests.form['filter']


html=req.text
header=req.headers
status=req.status_code
boolen=req.ok
##take information from http

soup=BeautifulSoup(html,'html.parser')
##html to python

condition_tag=soup.select(
    con
    )
##tag condition(will be more)

data={}

for i in condition_tag:
    data[i.text] = i.get('href')

@app.route('/result', methods = ['post'])

def result():
    return render_template('result.html',result = data)
##the location where the tags with filter conditions are to be stored

if __name__ == '__main__':
    app.run(debug = true)

with open(os.path.join(dir, 'result.json'), 'w+') as json_file:
    json.dump(data, json_file)
##save to result file at dir
