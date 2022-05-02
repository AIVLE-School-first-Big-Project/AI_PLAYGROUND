import dlib
import cv2
import numpy as np
import pandas as pd
import os
import requests
import json
import re
import shutil
import time
import datetime

face_detector = dlib.get_frontal_face_detector()
lower = np.array([0,133,77], dtype = np.uint8)
upper = np.array([255,173,127], dtype = np.uint8)
def detect_face_masking(image_path):
    img = cv2.imread(f'media/{image_path}')
    faces=[]
    try:
        faces = face_detector(img)
        print(faces)
    except:
        os.remove(f'media/{image_path}')
        image_path='fail'
    if len(faces) != 1 :
        os.remove(f'media/{image_path}')
        image_path='fail'
    else :
        f = faces[0]
        cropped_img = img[f.top()+2:f.bottom()-2, f.left()+2:f.right()-2]
        scalePercent = 0.3
        face_img_ycrcb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2YCrCb)
        skin_msk = cv2.inRange(face_img_ycrcb, lower, upper)
        skin = cv2.bitwise_and(cropped_img, cropped_img, mask = skin_msk)
        ratio_black = cv2.countNonZero(skin_msk)/(cropped_img.size/3)
        colorPercent = (ratio_black * 100) / scalePercent
        if colorPercent<=240:
            os.remove(f'media/{image_path}')
            image_path='fail'

        else:
            cv2.imwrite(f'media/{image_path}',skin)

    return image_path

