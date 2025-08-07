import cv2
import mediapipe as mp
import csv
from datetime import datetime

# 초기 설정
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

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
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        row = [frame_count]
        for lm in results.pose_landmarks.landmark:
            row += [lm.x, lm.y, lm.visibility]
        csv_writer.writerow(row)
        frame_count += 1

    cv2.imshow('Pose Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

f.close()
cap.release()
cv2.destroyAllWindows()
