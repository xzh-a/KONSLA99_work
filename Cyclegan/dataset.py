# Custom dataset
from PIL import Image
import torch.utils.data as data
import os
import random


class DatasetFromFolder(data.Dataset): # 이미지 디렉토리에서 이미지를 불러오는데 사용되는 사용자 정의 지정 데이터셋 클래스
    def __init__(self, image_dir, subfolder='train', transform=None, resize_scale=None, crop_size=None, fliplr=False):

        super(DatasetFromFolder, self).__init__()
        self.input_path = os.path.join(image_dir, subfolder)
        self.image_filenames = [x for x in sorted(os.listdir(self.input_path))] # 데이터 세트에 포함된 모든 이미지 파일 이름의 리스트를 저장합니다.
        self.transform = transform
        self.resize_scale = resize_scale
        self.crop_size = crop_size
        self.fliplr = fliplr

    def __getitem__(self, index):
        # Load Image
        img_fn = os.path.join(self.input_path, self.image_filenames[index])
        img = Image.open(img_fn).convert('RGB') # img_fn변수에 저장된 경로의 이미지를 rgb형식으로 변환하여 불러옴.

        # preprocessing
        if self.resize_scale:
            img = img.resize((self.resize_scale, self.resize_scale), Image.BILINEAR)

        if self.crop_size:
            x = random.randint(0, self.resize_scale - self.crop_size + 1) #이미지 크기 - 잘라낼 크기 / 이미지의 경계를 넘지 않도록 제한
            y = random.randint(0, self.resize_scale - self.crop_size + 1)
            img = img.crop((x, y, x + self.crop_size, y + self.crop_size))

        if self.fliplr:
            if random.random() < 0.5:
                img = img.transpose(Image.FLIP_LEFT_RIGHT) 
                # 난수가 0.5보다 작으면 이미지를 뒤집음. 이 확률적 filp은 데이터 셋 다양성을 높이고 모델 훈련 성능을 향상시키는 데 도움이 될 수     


        if self.transform is not None:
            img = self.transform(img)

        return img

    def __len__(self):
        return len(self.image_filenames)
