from flask import Flask, request
import tensorflow as tf
from models.transformers import transformer
import joblib
import re
import requests


app = Flask(__name__)

MAX_LENGTH = 40

NUM_LAYERS = 2
D_MODEL = 256
NUM_HEADS = 8
D_FF = 512
DROPOUT = 0.1

def preprocess_sentence(sentence):
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
    sentence = sentence.strip()
    return sentence

def get_sentence_ids(sentence):
    sentence = preprocess_sentence(sentence)

    encoded_sentence = tokenizer.encode(sentence)
    encoded_sentence = tf.expand_dims(START_TOKEN + encoded_sentence + END_TOKEN, axis=0)
    output = tf.expand_dims(START_TOKEN, 0)

    for i in range(MAX_LENGTH):
        prediction = model(inputs=[encoded_sentence, output], training=False)

        prediction = prediction[:, -1:, :]
        predicted_id = tf.cast(tf.argmax(prediction, axis=-1), tf.int32)

        if tf.equal(predicted_id, END_TOKEN[0]):
            break

        output = tf.concat([output, predicted_id], axis=-1)

    sentence_ids = tf.squeeze(output, axis=0)
    return sentence_ids


@app.route('/chatbot', methods=['POST'])
def get_chatbot_answer():
    if request.method == 'POST':
        try:
            user_text = request.form.get('user_text')
        except Exception as e:
            print(e)
            user_text = ''

        sentence_ids = get_sentence_ids(user_text)
        sentence_ids = [s for s in sentence_ids if s < tokenizer.vocab_size]

        chatbot_answer = tokenizer.decode(sentence_ids)
        input = {'chatbot_answer': chatbot_answer}
    
        try:
            response = requests.post('http://127.0.0.1:5003/predict', data=input)
            result = response.json()
        except:
            result = {'0':'0'}
    
        return {'message': chatbot_answer, 'wav': result}

    else:
        return {'chatbot_answer': 'Not POST'}


if __name__ == '__main__':
    tokenizer = joblib.load('models/tokenizer.pkl')
    START_TOKEN, END_TOKEN = [tokenizer.vocab_size], [tokenizer.vocab_size + 1]
    VOCAB_SIZE = tokenizer.vocab_size + 2
    
    model = transformer(vocab_size=VOCAB_SIZE, num_layers=NUM_LAYERS, d_ff=D_FF, d_model=D_MODEL, num_heads=NUM_HEADS, dropout=DROPOUT)
    model.load_weights('model_weights/model_weights')
    
    app.run(host='127.0.0.1', port=5002, debug=True)