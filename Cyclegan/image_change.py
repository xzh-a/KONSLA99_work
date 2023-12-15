import tkinter as tk
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
root.title("image_generator")
root.geometry("250x300")

# Label을 생성하여 현재 선택된 dataset을 표시합니다.
dataset_label = tk.Label(root, text="Selected Dataset: None")
dataset_label.pack()

# dataset 버튼을 생성합니다.
dataset_button_amature2master = tk.Button(root, text='amature2master', command=lambda: change_dataset('amature2master'))
dataset_button_amature2animation = tk.Button(root, text='amature2animation', command=lambda: change_dataset('amature2animation'))

# run 버튼을 생성합니다.
run_button = tk.Button(root, text='Run', command=run_image_generator)

# 버튼을 화면에 배치합니다.
dataset_button_amature2master.pack()
dataset_button_amature2animation.pack()
run_button.pack()

# "made by mingi chae"를 추가합니다.
made_by_label = tk.Label(root, text="Made by mingi chae")
made_by_label.pack()

# mainloop()를 호출하여 이벤트 루프를 시작합니다.
root.mainloop()
