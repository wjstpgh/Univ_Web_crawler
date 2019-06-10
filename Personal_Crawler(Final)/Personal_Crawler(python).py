import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, url_for
import json
import os

app = Flask(__name__, static_url_path='/static')

## 아무 값도 넘겨받지 않는 경우도 있으므로 비어 있는 url도 함께 mapping해주는 것이 필요함

@app.route('/')
def main_get(num=None):
    return render_template('submit_test.html',num=num)

## GET 방식으로 값을 전달받음
@app.route('/calculate', methods=['POST', 'GET'])
def calculate(num=None):
    if request.method == 'POST':
        #temp = request.form['char1']
        pass
    
    elif request.method == 'GET':
        dir = os.path.dirname(os.path.abspath(__file__))
        
        ##넘겨받은 웹사이트 주소 
        temp = request.args.get('char1')
        req = requests.get(''+temp)
        
        ##넘겨받은 태그 필터
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
        
        j = -19
        
        
        for i in condition_tag:
            ##네이버목차
            if '#PM_ID_themelist' in temp1:
                data[i.text] = i.get('href')
            ##각 목차에서 게시물에 대한 정보
            elif '.tl_default' in temp1:
                data[i.text.replace('\n','')] = ''
            ##네이버 인기검색어
            elif '.ah_k' in temp1:
                 data[i.text] = j
                 j = j+1
                
        ##데이터를 json파일로 저장해서 관리        
        with open(os.path.join(dir, 'result.json'), 'w+') as json_file:
            json.dump(data, json_file)
            
        ## 넘겨받은 값을 원래 페이지로 리다이렉트    
        return render_template('submit_test.html', char1=list(data.keys()), char2=list(data.values()))
    
if __name__ == '__main__':
    ## host주소를 설정함으로서 외부에서도 접속 가능하게 함.
    ## threaded=True 로 넘기면 multiple plot이 가능해짐
    app.run(host = '172.31.37.116', debug=True, threaded=True)