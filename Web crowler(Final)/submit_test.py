import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, url_for
import json
import os

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def main_get(num=None):
    return render_template('submit_test.html',num=num)

@app.route('/calculate', methods=['POST', 'GET'])
def calculate(num=None):
    if request.method == 'GET':
        dir = os.path.dirname(os.path.abspath(__file__))
        
        temp = request.args.get('char1')
        req = requests.get(''+temp)
        
        temp1 = request.args.get('char2')
        
        html=req.text
        header=req.headers
        status=req.status_code
        boolean=req.ok
        
        soup=BeautifulSoup(html,'html.parser')
        
        condition_tag=soup.select(
                temp1
        )
        
        data={}
        
        for i in condition_tag:
                data[i.text] = i.get('href')
        with open(os.path.join(dir, 'result.json'), 'w+') as json_file:
            json.dump(data, json_file)
            
        return render_template('submit_test.html', char1=list(data.keys()), char2=list(data.values()))
    
if __name__ == '__main__':
    app.run(host = '172.31.37.116', debug=True, threaded=True)