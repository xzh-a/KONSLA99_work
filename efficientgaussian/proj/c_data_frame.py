import cv2
import os

# 영상 파일 경로와 저장할 디렉토리 경로 설정
video_path = 'D:/code/3dgs/custom_data/25.sec.mp4'  # 저장된 영상 파일 경로
output_dir = 'D:/code/3dgs/custom_data/5frames'     # 저장할 이미지 폴더

# n번째 프레임마다 저장할 수 있도록 n 설정
n = 5  # 예: 10 프레임마다 저장

# 저장할 디렉토리가 없으면 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 영상 파일 열기
cap = cv2.VideoCapture(video_path)

frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break  # 영상이 끝나면 루프 종료

    # n번째 프레임마다 저장
    if frame_count % n == 0:
        frame_filename = f"{output_dir}/frame_{frame_count}.jpg"
        cv2.imwrite(frame_filename, frame)
        print(f"Saved {frame_filename}")

    frame_count += 1

# 캡쳐 종료
cap.release()
