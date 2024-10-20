import tflite_runtime.interpreter as tflite
import cv2
import numpy as np
import time
import os

# 파이프 파일 경로
pipe_name = '/tmp/my_pipe'

# 파이프가 존재하지 않으면 생성
if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the TensorFlow Lite model
tflite_interpreter = tflite.Interpreter(model_path="your_model.tflite")
tflite_interpreter.allocate_tensors()

# Get input and output tensors
input_details = tflite_interpreter.get_input_details()
output_details = tflite_interpreter.get_output_details()

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

# 파이프를 쓰기 모드로 열기
with open(pipe_name, 'w') as pipe:
    while True:
        # Grab the webcamera's image
        ret, image = camera.read()

        # Resize the raw image into (224-height,224-width) pixels
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

        # Show the image in a window
        cv2.imshow("Webcam Image", image)

        # Make the image a numpy array and reshape it to the model's input shape
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Set the value of the input tensor
        tflite_interpreter.set_tensor(input_details[0]['index'], image)

        # Run the model
        tflite_interpreter.invoke()

        # Get the prediction
        prediction = tflite_interpreter.get_tensor(output_details[0]['index'])
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

        # 파이프에 데이터 쓰기
        pipe_data = f"{str(np.round(confidence_score * 100))[:-2]} {class_name[2]}"
        pipe.write(pipe_data)
        pipe.flush()

        #time.sleep(0.1)

        # Listen to the keyboard for presses
        keyboard_input = cv2.waitKey(1)

        # 27 is the ASCII for the esc key on your keyboard
        if keyboard_input == 27:
            break

camera.release()
cv2.destroyAllWindows()

