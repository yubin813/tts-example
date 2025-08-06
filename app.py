from flask import Flask, render_template, request
# flask : 웹서버를 만들기 위한 Flask클래스
# render_template : html 파일을 연결해서 웹 페이지를 띄워줌
# request : 사용자(브라우저)가 보낸 데이터(입력값 등)을 받을 때 사용
from gtts import gTTS
# 구글의 TTS(Text-to-Speech)api를 사용하는 python라이브러리 -> 입력한 텍스트를 음성으로 바꿔주는 기능
import os
# os : 파일저장, 실행 등 운영체제 관련 기능 사용 (mp3파일 저장용)

app = Flask(__name__)
# --> Flask앱 생성
# __name__ 은 현재 실행되는 모듈의 이름(직접실행시__main__)
# -> 이코드를 통해 Flask 서버를 시작할 준비를 함

responses = {"혈압 측정": "혈압을 측정하겠습니다. 팔에 커프를 감아주세요.",
    "체온 확인": "체온을 측정하겠습니다. 이마에 센서를 대주세요.",
    "식사 알림": "지금은 식사 시간입니다. 맛있게 드세요!",
    "약 복용 알림": "약 드실 시간입니다. 처방에 따라 복용해주세요."}
# 사용자 명령어와 음성 응답을 짝지은 딕셔너리 형태
# 사용자가 입력한 명령어에 따라 적절한 멘트를 제공

# index는 웹사이트의 메인페이지(/) 처리
# route : uri정리, 연결시켜주는
# 일단 request가 오면 router가 받고 어떤 모델을 실행할지 판단
# 로그인 요청 -> 유저정보를 유저모델로 전달 -> 조건만족 -> 쿠키 
# @app.route('경로(url)', 'http메서드(get/post))
# @app은 .route()에 표시된 경로를 방문할때마다 hello_world()함수 실행
# 여러개의 경로설정 예를들면 
# @app.route('/')
# @app.route('/home')
# def hello_world():
#    return "ffff"
# --> 이렇게해도 각 다른 경로지만 같은 화면으로 표시된다.
# GET : 기본페이지 접속
# POST : 사용자입력을 서버로 보낼때 사용
@app.route('/', methods=['GET','POST'])
def index():
    message = ""
    #index()함수는 페이지를 렌더링할때 실행됨
    # message 는 사용자에게 보여줄 텍스트 응답 (html에서 사용됨)
    if request.method == 'POST':
        #사용자가 폼을 통해 명령어를 입력하고 보내기 버튼을 눌렀을때 실행
        command = request.form['command']
        # 폼에서 입력한 명령어를 가져옴
        # <input name = "command"> 의 값이 여기에 담김
        text = responses.get(command, "죄송합니다 이해할수없는 명령입니다.")
        # 사용자가 입력한 명령어가 responses 사전에 있으면 가져오고 아니면 오류문장반환

        tts = gTTS(text=text, lang='ko')
        # tts객체 생성
        # 저장된 texxt를 한국어 korea 으로 음성처리
        tts.save("static/response.mp3")
        # 음성으로만든 데이터를 mp3로 저장 static/폴더안에있는 파일을 웹에서 자동으로 읽을 수 있음

        message = f"응답:{text}"
        # 사용자에게 보여줄 메시지 설정 (웹페이지에서 출력되는 텍스트)
    return render_template('index.html', message=message)
    # index.html 이라는 html템플릿을 화면에 보여줌
    # 동시에 message라는 값을 전달해서 사용할수있게함

if __name__ == '__main__':
    # 이 파일을 직접 실행하면 Flask 서버를 시작
    app.run(debug=True)

