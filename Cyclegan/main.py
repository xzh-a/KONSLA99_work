import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys



# 전역 변수로 params 정의
params = {'dataset': None, 'direction': 'AtoB'}
custom_entry = None  # 전역 변수로 선언


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
    result_folder = os.path.join(os.path.dirname(sys.argv[0]), params['dataset'] + '_test_results', params['direction'])
    subprocess.run([sys.executable, 'D:/CYCLE_GAN/CycleGAN-1/image_generator.py', '--dataset', str(params['dataset'])])

def open_folder(folder_path):
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 실행 파일 내에서 실행 중이라면
        folder_path = os.path.join(sys._MEIPASS, folder_path)
    else:
        # PyInstaller 실행 파일이 아니라면
        folder_path = os.path.abspath(folder_path)

    os.startfile(folder_path)

def open_save_dir():
    save_dir = os.path.join(params['dataset'] + '_test_results', params['direction'])
    try:
        open_folder(save_dir)
    except FileNotFoundError:
        print(f"에러: 폴더 {save_dir}이(가) 존재하지 않습니다.")

def value_check(self):
    label.config(text="숫자를 입력하세요.")
    valid = False
    if self.isdigit():
        if (int(self) <= 50 and int(self) >= 0):
            valid = True
    elif self == '':
        valid = True
    return valid

def value_error(self):
    label.config(text=str(self) + "를 입력하셨습니다.\n올바른 값을 입력하세요.")



def open_custom_dir():
    custom_dir = custom_entry.get()
    base_path = "D:\CYCLE_GAN\CycleGAN-1/amature2master_test_results\AtoB"  # 슬래시로 경로를 지정
    combined_path = os.path.join(base_path, custom_dir).replace("\\","/")
    print(f"",combined_path)
    

   
    # img_result_path를 그대로 전달
    subprocess.run([sys.executable, 'D:\CYCLE_GAN\CycleGAN-1\edge.py', combined_path])


    

root = tk.Tk()
root.title("CycleGan project")
root.geometry("300x350")

label = tk.Label(root, text="")
label.pack()

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

# A폴더가 input임을 알리기 위한 설명
label = tk.Label(root, text="input data=A")
label.pack()

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
obj = tk.Frame(root)
open_save_dir_button = ttk.Button(obj, text='이미지 확인', command=open_save_dir)
open_obj_dir_button = ttk.Button(obj, text='obj')
open_save_dir_button.grid(row=1, column=0, padx=(0, 5))  # 여백을 추가합니다.
open_obj_dir_button.grid(row=1, column=1)

# 사용자 지정 경로 Entry 및 확인 버튼
custom_entry_label = ttk.Label(obj, text="이미지 선택:")
custom_entry_label.grid(row=2, column=0, padx=(0, 5))  # 여백을 추가합니다.

custom_entry = ttk.Entry(obj)
custom_entry.grid(row=2, column=1)

custom_button = ttk.Button(obj, text="확인", command=open_custom_dir)
custom_button.grid(row=2, column=2)

# obj 프레임 내에서 가운데 정렬을 위한 설정
obj.grid_columnconfigure(0, weight=1)
obj.grid_columnconfigure(1, weight=1)
obj.grid_rowconfigure(1, weight=1)

obj.pack()

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
