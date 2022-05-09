import tensorflow as tf
import cv2
import dlib
import numpy as np
import matplotlib.pyplot as plt
import os
from glob import glob
from ugatit import UGATIT

tf.logging.set_verbosity(tf.logging.ERROR)
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('checkpoint/shape_predictor_5_face_landmarks.dat')

checkpoint_path = 'checkpoint/UGATIT_selfie2anime_lsgan_4resblock_6dis_1_1_10_10_1000_sn_smoothing/UGATIT.model-1000000'

sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))

gan = UGATIT()
gan.build_model()
saver = tf.train.Saver()
saver.restore(sess, checkpoint_path)

def selfie2anime(img_path):
    img = cv2.imread(img_path, flags=cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    brightness = 0
    contrast = 30
    img = np.int16(img)
    img = img * (contrast / 127 + 1) - contrast + brightness
    img = np.clip(img, 0, 255)
    img = np.uint8(img)

    dets = detector(img)
    
    if len(dets) == 0:
        result = 'No faces!'
    else:
        # don't crop if face is too big
        if dets[0].width() < img.shape[1] * 0.55:
            s = sp(img, dets[0])
            img = dlib.get_face_chip(img, s, size=256, padding=0.65)

        # preprocessing
        img_input = cv2.resize(img, dsize=(256, 256), interpolation=cv2.INTER_NEAREST)
        img_input = np.expand_dims(img_input, axis=0)
        img_input = img_input / 127.5 - 1

        # inference
        img_output = sess.run(gan.test_fake_B, feed_dict={gan.test_domain_A: img_input})

        # postprocessing
        img_output = (img_output + 1) * 127.5
        img_output = img_output.astype(np.uint8).squeeze()
        
        result = np.hstack([cv2.resize(img, (256, 256)), img_output])

        cv2.imwrite('static/%s' % os.path.basename(img_path), result[:, :, ::-1])

    return result