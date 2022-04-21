import io
import json
import os
from flask.templating import render_template
from flask import Flask, jsonify, request, redirect
#from flask_ngrok import run_with_ngrok
import transform

app = Flask(__name__)

@app.route('/api',methods=['POST'])
def predict():
    f = request.

