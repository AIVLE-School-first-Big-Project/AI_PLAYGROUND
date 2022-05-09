# 이용방법

## 설정 환경

- conda create -n ugatit python=3.7
- conda activate ugatit
- pip install -r requirements.txt
- conda install -c conda-forge dlib
- python app.py

## 모델 불러오기

- 가중치 모델의 용량이 약 7GB 이므로 github에 올려지지 않습니다.
- 따라서 아래 파일을 다운 후 /checkpoint 경로를 만들고 이곳에 아래 파일을 넣어주세요
- [https://drive.google.com/file/d/1fC4kbsQqZ-pBRLkU3MHfaA1H1AFJgma1/view?usp=sharing](https://drive.google.com/file/d/1fC4kbsQqZ-pBRLkU3MHfaA1H1AFJgma1/view?usp=sharing)

## API 호출법

- conda activate ugatit
- python [app.py](http://app.py)
- cd (이미지가 있는 경로)
- curl -X POST -F file=@{사진이름} http://127.0.0.1:5000/predict
    - ex) curl -X POST -F file=@js.jpg http://127.0.0.1:5000/predict
- (하지만 장고 연동으로 굳이 하지 않아도 됩니다.)

## 모델 Architecture

<img src = 'https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FvXlZl%2FbtqYbIBtsmR%2FOtEJweMsF5kfVltONPDBJ0%2Fimg.png' width=600 height=600 >
