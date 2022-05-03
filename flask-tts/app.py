from flask_restful import reqparse
from flask import Flask
import glob
from jamo import hangul_to_jamo
import librosa
from models.modules import griffin_lim
from models.tacotron import Tacotron
from models.tacotron import post_CBHG
import numpy as np
import os
import scipy
import soundfile as sf
import torch
from util.text import text_to_sequence
from util.hparams import *

app = Flask(__name__)

checkpoint_dir1 = './ckpt/ckpt-200000.pt'
checkpoint_dir2 = './ckpt/ckpt-228000.pt'
save_dir = './output'
send_dir = './output/0.wav'
os.makedirs(save_dir, exist_ok=True)

def inference1(text, idx):
    seq = text_to_sequence(text)
    enc_input = torch.tensor(seq, dtype=torch.int64).unsqueeze(0)
    sequence_length = torch.tensor([len(seq)], dtype=torch.int32)
    dec_input = torch.from_numpy(np.zeros((1, mel_dim), dtype=np.float32))

    pred, alignment = model1(enc_input, sequence_length,
                             dec_input, is_training=False, mode='inference')
    pred = pred.squeeze().detach().numpy()
    alignment = np.squeeze(alignment.detach().numpy(), axis=0)

    np.save(os.path.join(save_dir, 'mel-{}'.format(idx)),
            pred, allow_pickle=False)

def inference2(text, idx):
    mel = torch.from_numpy(text).unsqueeze(0)
    pred = model2(mel)
    pred = pred.squeeze().detach().numpy() 
    pred = np.transpose(pred)
    
    pred = (np.clip(pred, 0, 1) * max_db) - max_db + ref_db
    pred = np.power(10.0, pred * 0.05)
    wav = griffin_lim(pred ** 1.5)
    wav = scipy.signal.lfilter([1], [1, -preemphasis], wav)
    wav = librosa.effects.trim(wav, frame_length=win_length, hop_length=hop_length)[0]
    wav = wav.astype(np.float32)
    # sf.write(os.path.join(save_dir, '{}.wav'.format(idx)), wav, sample_rate)
    return [sample_rate] + list(wav)

@app.route('/predict', methods=['POST'])
def predict():

    parser = reqparse.RequestParser()
    parser.add_argument('chatbot_answer', action='append')

    args = parser.parse_args()
    sentences = args['chatbot_answer']
    for i, text in enumerate(sentences):
        jamo = ''.join(list(hangul_to_jamo(text.replace('.', '').replace('!', '').replace('?', '').replace(',', ''))))
        inference1(jamo, i)

    mel_list = glob.glob(os.path.join(save_dir, '*.npy'))

    result = {}
    for i, fn in enumerate(mel_list):
        mel = np.load(fn)
        for j, k in enumerate(inference2(mel, i)):
            result[j] = str(k)

    return result

if __name__ == '__main__':

    model1 = Tacotron(K=16, conv_dim=[128, 128])
    ckpt1 = torch.load(checkpoint_dir1, map_location=torch.device('cpu'))
    model1.load_state_dict(ckpt1['model'])
    model2 = post_CBHG(K=8, conv_dim=[256, mel_dim])
    ckpt2 = torch.load(checkpoint_dir2, map_location=torch.device('cpu'))
    model2.load_state_dict(ckpt2['model'])

    app.run(host='127.0.0.1', port=5003, debug=True)
