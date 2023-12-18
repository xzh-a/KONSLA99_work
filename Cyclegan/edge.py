import numpy as np, cv2
import main
import cv2
import matplotlib.pyplot as plt
import shutil
import sys



def nonmax_suppression(sobel, direct):
    rows, cols = sobel.shape[:2]
    dst = np.zeros((rows, cols), np.float32)
    for i in range(1, rows-1):
        for j in range(1, cols-1):
          
            values = sobel[i-1:i+2, j-1:j+2].flatten()
            first = [3, 0, 1, 2]
            id = first[direct[i, j]]
            v1, v2 = values[id], values[8-id]


      
            dst[i, j] = sobel[i, j] if (v1 < sobel[i, j] > v2) else 0
    return dst

def trace(max_sobel, i, j, low):
    h, w = max_sobel.shape
    if (0 <= i < h and 0 <= j < w) == False: return
    if pos_ck[i, j] > 0 and max_sobel[i, j] > low:
        pos_ck[i, j] = 255
        canny[i, j] = 255

        trace(max_sobel, i-1, j-1, low)
        trace(max_sobel, i, j-1, low)
        trace(max_sobel, i+1, j-1, low)
        trace(max_sobel, i-1, j, low)
        trace(max_sobel, i+1, j, low)
        trace(max_sobel, i-1, j+1, low)
        trace(max_sobel, i, j+1, low)
        trace(max_sobel, i+1, j+1, low)

def hysteresis_th(max_sobel, low, high):
    rows, cols = max_sobel.shape[:2]
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            if max_sobel[i, j] >= high: trace(max_sobel, i, j, low)



image_path = "C:/Users/vtoree/Desktop/CYCLE_GAN/imgpath/iphone.jpg"




image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

image = cv2.resize(image, (321, 600))

image_c = cv2.imread(image_path, cv2.IMREAD_COLOR)
image_c = cv2.resize(image_c, (321, 600))   

image_c_rgb = cv2.cvtColor(image_c, cv2.COLOR_BGR2RGB)


plt.imshow(image_c_rgb)
plt.axis('off')  
plt.show()



pos_ck = np.zeros(image.shape[:2], np.uint8)
canny = np.zeros(image.shape[:2], np.uint8)


gaus_img = cv2.GaussianBlur(image, (5, 5), 0.3)
plt.imshow(gaus_img)
plt.axis('off')  
plt.show()

#cv2.imshow("gaussian", gaus_img)
Gx = cv2.Sobel(np.float32(gaus_img), cv2.CV_32F, 1, 0, 3)
Gy = cv2.Sobel(np.float32(gaus_img), cv2.CV_32F, 0, 1, 3)

# Gx = cv2.convertScaleAbs(Gx)
# Gy = cv2.convertScaleAbs(Gy)

sobel = cv2.magnitude(Gx, Gy)
sobel = np.clip(sobel, 0, 255).astype(np.uint8)
print(f"<sobel>\화소값 총합 : {cv2.sumElems(sobel)} \n화소 최대값 : {np.max(sobel)} \n화소 최소값 : {np.min(sobel)} \n행렬형태: {sobel.shape}")

directs = cv2.phase(Gx, Gy) / (np.pi/4)
directs = directs.astype(int) % 4
max_sobel = nonmax_suppression(sobel, directs)
max_sobel = max_sobel.astype(np.uint8)
print(f"<max_sobel>\n화소값 총합 : {cv2.sumElems(max_sobel)} \n화소 최대값 : {np.max(max_sobel)} \n화소최소값 : {np.min(max_sobel)} \n행렬형태 : {max_sobel.shape}")


plt.imshow(max_sobel)
plt.axis('off')  
plt.show()

print(sobel >= max_sobel)
checker = sobel >= max_sobel
unique, counts = np.unique(checker, return_counts=True)
checker = dict(zip(unique, counts))
print(checker)

m = 0
n = 0
print(f"sobel의 화소값 : {sobel[m, n]} \nmax_sobel의 화소값 : {max_sobel[m, n]}")

nonmax = max_sobel.copy()


hysteresis_th(max_sobel, 100, 150)

print(nonmax)
print(max_sobel)
print(nonmax == max_sobel)

canny = max_sobel.copy()
canny2 = cv2.Canny(image, 100, 150)


canny = cv2.Canny(image, 100, 150, apertureSize=3)  # apertureSize 매개변수 추가

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
sobel_rgb = cv2.cvtColor(sobel, cv2.COLOR_BGR2RGB)
canny_rgb = cv2.cvtColor(canny, cv2.COLOR_BGR2RGB)
canny2_rgb = cv2.cvtColor(canny2, cv2.COLOR_BGR2RGB)

# 이미지 표시
plt.subplot(221), plt.imshow(image_rgb, cmap='gray'), plt.title('Original Image')
plt.subplot(222), plt.imshow(sobel_rgb, cmap='gray'), plt.title('Sobel')
plt.subplot(223), plt.imshow(canny_rgb, cmap='gray'), plt.title('Canny')
plt.subplot(224), plt.imshow(canny2_rgb, cmap='gray'), plt.title('OpenCV Canny')

plt.show()




# 등고선 찾기
contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 등고선 중 가장 큰 것 선택
largest_contour = max(contours, key=cv2.contourArea)

# 등고선을 감싸는 최소 사각형 구하기
x, y, w, h = cv2.boundingRect(largest_contour)

# 등고선 내부의 작은 등고선들 찾기
inner_contours = []
for contour in contours:
    if cv2.contourArea(contour) < cv2.contourArea(largest_contour):
        inner_contours.append(contour)

# 작은 등고선들도 포함하는 최소 사각형 계산
for inner_contour in inner_contours:
    x_inner, y_inner, w_inner, h_inner = cv2.boundingRect(inner_contour)
    x = min(x, x_inner)
    y = min(y, y_inner)
    w = max(x + w, x_inner + w_inner) - x
    h = max(y + h, y_inner + h_inner) - y

# 이미지 잘라내기
result_crop = canny_rgb[y:y+h, x:x+w]

# 결과 이미지 표시
plt.imshow(result_crop)
plt.axis('off')
plt.show()





#print(f"",image_path_A_drive)
image_path_A_drive = "D:/CYCLE_GAN/CycleGAN-1/amature2master_test_results/AtoB/Test_result_9.png"
image_A = cv2.imread(image_path_A_drive)





# 이미지 크기 조절 (이미지 크기가 같아야 함)
image_A = cv2.resize(image_A, (result_crop.shape[1], result_crop.shape[0]))

# 이미지를 반투명하게 합치기
alpha = 0.5  # 조절 가능한 투명도 값
result = cv2.addWeighted(result_crop, 1 - alpha, image_A, alpha, 0)

# 이미지 표시
plt.imshow(result)
plt.axis('off')
plt.show()


# 여백 크기 설정
padding_top = y
padding_bottom = canny_rgb.shape[0] - (y + result.shape[0])
padding_left = x
padding_right = canny_rgb.shape[1] - (x + result.shape[1])

# 이미지 주변에 여백 추가
result_padded = cv2.copyMakeBorder(result, padding_top, padding_bottom, padding_left, padding_right, cv2.BORDER_CONSTANT, value=0)

# 결과 이미지 표시
plt.imshow(result_padded)
plt.axis('off')
plt.show()





# 엣지 검출 결과 이미지를 이진 이미지로 변환
canny_bin = cv2.threshold(canny, 128, 255, cv2.THRESH_BINARY)[1]

# 엣지가 있는 부분의 외곽선 찾기
contours, _ = cv2.findContours(canny_bin, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)



# 엣지 검출 결과 이미지를 이진 이미지로 변환
canny_bin = cv2.threshold(canny, 128, 255, cv2.THRESH_BINARY)[1]

# 엣지가 있는 부분의 외곽선 찾기
contours, _ = cv2.findContours(canny_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 외곽선 중에서 가장 큰 부분 선택
largest_contour = max(contours, key=cv2.contourArea)
smallest_contour = min(contours, key = cv2.contourArea)



# 외곽선을 감싸는 사각형 좌표 계산
x, y, w, h = cv2.boundingRect(largest_contour)

# 이미지를 자를 부분을 나타내는 마스크 생성
mask = np.zeros_like(canny_bin)
cv2.drawContours(mask, [largest_contour], 0, (255), thickness=cv2.FILLED)

# 마스크를 이용하여 이미지 자르기
result_cropped = cv2.bitwise_and(result_padded, result_padded, mask=mask)



# 결과 이미지 표시
plt.imshow(result_cropped)
plt.axis('off')
plt.show()





result_rgb = cv2.cvtColor(result_cropped, cv2.COLOR_BGR2RGB)
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
result_rgb = cv2.resize(result_rgb, (image.shape[1], image.shape[0]))
plt.imshow(result_rgb)
plt.axis('off')
plt.show()












