
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import transform
import json 

app = Flask(__name__)

@app.route('/predict', methods = ['POST'])
def file_upload():
    f = request.files['file']
    filename = f.filename
    f.save('imgs/' + secure_filename(filename))
    f2 = transform.selfie2anime('imgs/' + filename)
    result_dict = {}
    if f2 == 'No faces!':
        result_dict['try'] = 'No faces!'
    else:
        result_dict['try'] = 'success'
        # result_dict['resultfile'] = '../flask-ani/static/' + filename
    result_dict = json.dumps(result_dict)
    return jsonify(result_dict)
    
if __name__ == '__main__':
    app.run(port="5001", debug = True)