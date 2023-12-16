import tkinter as tk
from tkinter import ttk
import subprocess
import os

# 전역 변수로 params 정의
params = {'dataset': None, 'direction': 'AtoB'}

def change_dataset(dataset):
    params['dataset'] = dataset
    dataset_label.config(text=f"선택된 스타일 변환: {dataset}")

def change_direction(direction):
    params['direction'] = direction
    direction_label.config(text=f"선택된 폴더: {direction}")

def run_image_generator():
    print('dataset:', params['dataset'])
    print('direction:', params['direction'])
    dataset_label.config(text=f"선택된 데이터셋: {params['dataset']}")
    direction_label.config(text=f"선택된 방향: {params['direction']}")
    result_folder = os.path.join(params['dataset'] + '_test_results', params['direction'])
    subprocess.run(['python', 'D:/CYCLE_GAN/CycleGAN-1/image_generator.py', '--dataset', str(params['dataset'])])

def open_folder(folder_path):
    os.startfile(folder_path)

def open_save_dir():
    save_dir = os.path.join(params['dataset'] + '_test_results', params['direction'])
    try:
        open_folder(os.path.abspath(save_dir))
    except FileNotFoundError:
        print(f"에러: 폴더 {save_dir}이(가) 존재하지 않습니다.")

root = tk.Tk()
root.title("CycleGan project")
root.geometry("300x350")

# 데이터셋 표시
dataset_label = ttk.Label(root, text="선택된 스타일변환: None")
dataset_label.pack()

# 데이터셋 버튼
frame_dataset = tk.Frame(root)
dataset_button_amature2master = ttk.Button(frame_dataset, text='amature2master', command=lambda: change_dataset('amature2master'))
dataset_button_amature2animation = ttk.Button(frame_dataset, text='amature2animation', command=lambda: change_dataset('amature2animation'))
dataset_button_amature2master.grid(row=0, column=0, padx=(0, 5))  # 여백을 추가합니다.
dataset_button_amature2animation.grid(row=0, column=1)
frame_dataset.pack()

# 실행 버튼
run_button = ttk.Button(root, text='이미지 생성', command=run_image_generator)
run_button.pack()

# 버튼과 레이블 사이에 여백을 추가
separator1 = ttk.Separator(root, orient="horizontal")
separator1.pack(fill="x", padx=5, pady=5)

# 확인할 폴더
frame_direction = tk.Frame(root)
direction_button_atob = ttk.Button(frame_direction, text='AtoB', command=lambda: change_direction('AtoB'))
direction_button_btoa = ttk.Button(frame_direction, text='BtoA', command=lambda: change_direction('BtoA'))
direction_button_atob.grid(row=1, column=0, padx=(0, 5))  # 여백을 추가합니다.
direction_button_btoa.grid(row=1, column=1)
frame_direction.pack()

# 확인할 폴더 label
direction_label = ttk.Label(root, text="선택된 폴더: AtoB")
direction_label.pack()



# Open 버튼
open_save_dir_button = ttk.Button(root, text='이미지 확인', command=open_save_dir)
open_save_dir_button.pack()

# 버튼과 레이블 사이에 여백을 추가
separator2 = ttk.Separator(root, orient="horizontal")
separator2.pack(fill="x", padx=5, pady=5)

# 프로젝트 제작자 정보
made_by_label = ttk.Label(root, text="제작자: 채민기")
made_by_label.pack()
made_by_label = ttk.Label(root, text="     이정훈")
made_by_label.pack()
made_by_label = ttk.Label(root, text="     이정우")
made_by_label.pack()

# mainloop()를 호출
root.mainloop()
