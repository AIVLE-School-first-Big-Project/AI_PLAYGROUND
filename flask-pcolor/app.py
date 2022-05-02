import os
from flask import Flask,redirect,url_for,request,render_template,jsonify
import model,detect
import json 
app = Flask(__name__)
@app.route('/colorpredict', methods=['POST','GET'])
def predict():
    if request.method=='POST':
        f=request.files['file']
        filename = f.filename
        f.save('media/'+str(filename))
        f_path = str(filename)
        print(f_path)
        result=detect.detect_face_masking(f_path)
        result_dict={
            'pcolor' : 'fail'
        }
        if result!='fail':
            result=model.predict_pcolor(result)
            result_dict = {
            'pcolor' : str(result),
        }
        result_dict = json.dumps(result_dict)
        return jsonify(result_dict)

    

if __name__ == "__main__":
    app.run(debug=True)
