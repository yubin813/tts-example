import cv2
# OpenCV 라이브러리 불러오기(카메라제어, 영상처리용)
import mediapipe as mp
# MediaPipe라이브러리를 불러옴 (자세 추정, 손/얼굴 인식 등에 사용됨)
import csv
from datetime import datetime

# 초기 설정
mp_pose = mp.solutions.pose
# MediaPipe는 Pose의 모듈을 사용하겠다고 선언, mp_pose는 자세인식기능을 담당함
pose = mp_pose.Pose()
# pose라는 이름으로 MediaPipe자세 추정 모델을 초기화함
# 내부적으로는 ai모델이 메모리에 올라옴
mp_drawing = mp.solutions.drawing_utils
# MediaPipe에서 제공하는 그리기 도구 모음
# 사람 관절을 선으로 연결해서 영상위에 시각화할때 사용

# CSV 저장용
filename = f"pose_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
f = open(filename, 'w', newline='')
csv_writer = csv.writer(f)
header = ['frame']
for i in range(33):  # 33개의 관절
    header += [f'x{i}', f'y{i}', f'visibility{i}']
csv_writer.writerow(header)

# 웹캠
cap = cv2.VideoCapture(0)
# 기본 웹캠(0)을 통해 양싱입력받기시작
# cap.read()로 매 프레임 읽을수있음
frame_count = 0

while cap.isOpened():
    # 카메라가 정상적으로 열려있으면 반복수행
    ret, frame = cap.read()
    if not ret:
        break
        # 영상읽기에 실패하면 반복종료
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # OpenCV와 달리 RGB형식만받음 변환
    results = pose.process(image)
    # 변환된 이미지를 MdiaPipe pose에 입력
    # 결과로 사람관절좌표가 results에 저장됨

    if results.pose_landmarks:
        #사람관절이 감지되었는지 확인
        # 사람이 없으면 아무것도 그리지 않음
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        row = [frame_count]
        for lm in results.pose_landmarks.landmark:
            row += [lm.x, lm.y, lm.visibility]
        csv_writer.writerow(row)
        frame_count += 1
        # 사람의 관절을 선으로 연결해서 frame위에 시각화

    cv2.imshow('Pose Detection', frame)
    # 현재 프레임을 화면에 띄움
    # 'MediaPipe Pose'창에서 실시간확인가능

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

f.close()
cap.release()
cv2.destroyAllWindows()
