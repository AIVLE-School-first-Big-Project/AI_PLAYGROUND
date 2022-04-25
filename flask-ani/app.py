
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import transform

app = Flask(__name__)

@app.route('/predict', methods = ['POST'])
def file_upload():
    f = request.files['file']
    filename = f.filename
    f.save('imgs/' + secure_filename(filename))
    f2 = transform.selfie2anime('imgs/' + filename)
    
    result_dict = {
        'name' : str(filename),
    }
    return '파일이 저장되었습니다'
    
if __name__ == '__main__':
    app.run(port="5000", debug = True)