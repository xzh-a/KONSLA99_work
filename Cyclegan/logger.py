
import tensorflow as tf
import numpy as np
import imageio
from io import BytesIO  # Python 3.x


class Logger(object):
    def __init__(self, log_dir):
        """Create a summary writer logging to log_dir."""
        self.writer = tf.summary.create_file_writer(log_dir)

    def scalar_summary(self, tag, value, step):

        #   tag: 스칼라 값의 이름.value: 스칼라 값. step: 훈련 스텝.
        """Log a scalar variable."""
        with self.writer.as_default():
            tf.summary.scalar(tag, value, step=step)
            self.writer.flush()

    def image_summary(self, tag, images, step):
        """Log a list of images."""
        with self.writer.as_default():
            img_summaries = []
            for i, img in enumerate(images):
                #이미지를 디스크에 저장 /tag:이름 / i:인덱스 / step: 훈련스텝
                imageio.imwrite(f"D:/CYCLE_GAN/CycleGAN-1/Train_result/{tag}_{i}_{step}.png", img)

                # tf.io.read_file -> 이미지 읽어오고 -> tf.image.decode_image() - > 텐서로 변환
                # rgb이미지로 해석 하기 위하여 channel을 3으로 설정
                img_sum = tf.image.decode_image(tf.io.read_file(f"D:/CYCLE_GAN/CycleGAN-1/Train_result/{tag}_{i}_{step}.png"), channels=3)
                img_sum = tf.expand_dims(img_sum, 0)  #이미지 텐서를 텐서보드에 기록하기위하여 배치 차원 추가해서 3차원 텐서로 변환
                #이미지요약
                tf.summary.image('%s/%d' % (tag, i), img_sum, step=step)
                

                #리스트에  훈련 과정 중에 생성된 모든 이미지 요약 텐서를 저장
                img_summaries.append(img_sum)

            #기록된 데이터를 텐서보드에 반영
            self.writer.flush()

    def histo_summary(self, tag, values, step, bins=1000):
        # bin은 데이터 값의 범위를 세분화하여 표현하는 구간,빈 개수가 많으면 더 상세한 분포를 확인할 수 있지만, 빈 개수가 적으면 더 일반적인 분포를 확인할 수 있음.
        """Log a histogram of the tensor of values."""
        with self.writer.as_default():
            tf.summary.histogram(tag, values, step=step, buckets=bins) #히스토 그램 요약 생성
            self.writer.flush() # 텐서보드에 기록
