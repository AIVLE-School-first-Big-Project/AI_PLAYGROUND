import io
import json
import os
from flask.templating import render_template
from flask import Flask, jsonify, request, redirect, send_file
import numpy as np
#from flask_ngrok import run_with_ngrok
import transform
import base64
#from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
app = Flask(__name__)
#run_with_ngrok(app)


# 이미지 직접출력 
@app.route('/predict', methods=['POST'])
def predict():
    if request.method=='POST':
        f=request.files['file']
        print(f)
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


        return 'success'
        #return jsonify(result_dict)

if __name__ == "__main__":
    app.run(debug=True)