import io
import json
import os
from flask.templating import render_template
from flask import Flask, jsonify, request, redirect
import numpy as np
#from flask_ngrok import run_with_ngrok
import transform
import base64
#from flask_ngrok import run_with_ngrok
app = Flask(__name__)
#run_with_ngrok(app)


@app.route('/upload')
def upload_file():
    return render_template('upload.html')

# 이미지 직접출력 
@app.route('/uploader', methods=['GET','POST'])
def uploader_file():
    if request.method=='POST':
        f=request.files['file']
        filename = f.filename
        f.save(str(filename))
        f_path = str(filename)
        print(f_path)
        result = transform.selfie2anime(f_path)
        result_dict = {
            'name' : str(filename),
            'image_dict': result.tolist()
        }
        result_dict = json.dumps(result_dict)


        return render_template('test.html', filename=f_path)
        #return jsonify(result_dict)



# @app.route('/predict', method=['POST'])
# def predict():
#     if request.method == 'POST':
#         # 이미지 바이트 데이터 받아오기
#         file = request.files['file']
#         result = transform.selfie2anime(file)
#         print(result)
#         return result


if __name__ == "__main__":
    app.run(debug=True)
