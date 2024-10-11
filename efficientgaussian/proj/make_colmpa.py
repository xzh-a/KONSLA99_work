import cv2
import os

# 비디오 파일 경로
video_path = 'D:/code/git hub repository/minigi-chae/efficientgaussian/custom_data/25.sec.mp4'
# 저장할 경로
output_path = 'D:/code/git hub repository/minigi-chae/efficientgaussian/custom_data/5frames_colmap'
# 프레임 추출 주기 (매 5프레임마다 저장)
frame_interval = 5  

# 출력 디렉토리 생성
if not os.path.exists(output_path):
    os.makedirs(output_path)

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_path)

# 비디오가 성공적으로 열렸는지 확인
if not cap.isOpened():
    print("Error: Could not open video.")
else:
    print("Video opened successfully.")
    
    # 프레임 초기화
    frame_count = 0
    saved_frame_count = 0  # 초기화

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No frame captured. End of video or error.")
            break  # 비디오의 끝에 도달

        # 특정 주기마다 프레임 저장
        if frame_count % frame_interval == 0:
            # 이미지 파일 이름 생성
            frame_filename = os.path.join(output_path, f"frame_{saved_frame_count:04d}.png")
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1  # 프레임 저장 카운트 증가
            print(f"Saved frame: {frame_filename}")  # 저장된 프레임 출력

        frame_count += 1

    # 비디오 캡처 객체 해제
    cap.release()

# 저장된 프레임 수 출력
print(f"Total {saved_frame_count} frames saved to {output_path}.")
