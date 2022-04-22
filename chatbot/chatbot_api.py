from flask_restful import reqparse
from flask import Flask
import tensorflow as tf
from transformers import AutoTokenizer
from transformers import TFGPT2LMHeadModel
import joblib

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world!"


@app.route('/chatbot', methods=['POST'])
def get_chatbot_answer():
    
    parser = reqparse.RequestParser()
    parser.add_argument('user_text')
    arg = parser.parse_args()
    
    user_sentence = '<usr>' + arg['user_text'] + '<sys>'
    input_ids = [tokenizer.bos_token_id] + tokenizer.encode(user_sentence)
    input_ids = tf.convert_to_tensor([input_ids])
    
    output_ids = model.generate(input_ids, max_length=32, do_sample=True, top_k=20)
    chatbot_sentence = tokenizer.decode(output_ids[0].numpy().tolist())
    chatbot_answer = chatbot_sentence.split('<sys> ')[1].replace('</s>', '')
    result = {'chatbot_answer': chatbot_answer}
    
    return result


if __name__ == '__main__':
    tokenizer = joblib.load('model/tokenizer.pkl')
    model = TFGPT2LMHeadModel.from_pretrained('model/tf_model')
    
    app.run(host='127.0.0.1', port=5000, debug=True)
