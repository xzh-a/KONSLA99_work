import tkinter as tk
from tkinter import ttk
import subprocess

# 전역 변수로 params 정의
params = {'dataset': None}

def change_dataset(dataset):
    # dataset 값을 변경합니다.
    params['dataset'] = dataset
    # 변경된 dataset 값을 텍스트로 업데이트합니다.
    dataset_label.config(text=f"Selected Dataset: {dataset}")

def run_image_generator():
    # 변경된 dataset 값을 출력합니다.
    print('dataset:', params['dataset'])
    # 변경된 dataset 값을 텍스트로 업데이트합니다.
    dataset_label.config(text=f"Selected Dataset: {params['dataset']}")
    # image_generator.py를 실행합니다.
    subprocess.run(['python', 'D:/CYCLE_GAN/CycleGAN-1/image_generator.py', '--dataset', str(params['dataset'])])

root = tk.Tk()
root.title("CycleGan Project")
root.geometry("250x300")

# Label을 생성하여 현재 선택된 dataset을 표시합니다.
dataset_label = ttk.Label(root, text="Selected Dataset: None")
dataset_label.pack()

# dataset 버튼을 생성합니다.
frame = tk.Frame(root)

dataset_button_amature2master = ttk.Button(frame, text='amature2master', command=lambda: change_dataset('amature2master'))
dataset_button_amature2animation = ttk.Button(frame, text='amature2animation', command=lambda: change_dataset('amature2animation'))

dataset_button_amature2master.grid(row=0, column=0)
dataset_button_amature2animation.grid(row=0, column=1)

frame.pack()

# 스타일을 적용합니다.
style = ttk.Style()
style.configure('mystyle.TButton', background='#0000ff', foreground='#000000', relief='raised')

# 스타일을 적용합니다.
dataset_button_amature2master.config(style='mystyle.TButton')
dataset_button_amature2animation.config(style='mystyle.TButton')

# run 버튼을 생성합니다.
run_button = ttk.Button(root, text='Run', command=run_image_generator)

# 버튼을 화면에 배치합니다.
run_button.pack()

# WHO MADE THIS PROJECT
made_by_label = ttk.Label(root, text="Made by MIN GI CHAE")
made_by_label.pack()
made_by_label = ttk.Label(root, text="         JUNG HOON LEE")
made_by_label.pack()
made_by_label = ttk.Label(root, text="         JUNG WOO LEE")
made_by_label.pack()

# mainloop()를 호출하여 이벤트 루프를 시작합니다.
root.mainloop()
