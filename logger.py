
import tensorflow as tf
import numpy as np
import imageio
from io import BytesIO  # Python 3.x


class Logger(object):
    def __init__(self, log_dir):
        """Create a summary writer logging to log_dir."""
        self.writer = tf.summary.create_file_writer(log_dir)

    def scalar_summary(self, tag, value, step):
        """Log a scalar variable."""
        with self.writer.as_default():
            tf.summary.scalar(tag, value, step=step)
            self.writer.flush()

    def image_summary(self, tag, images, step):
        """Log a list of images."""
        with self.writer.as_default():
            img_summaries = []
            for i, img in enumerate(images):
                # 이미지를 파일에 쓰기
                imageio.imwrite(f"D:/CYCLE_GAN/CycleGAN-1/Train_result/{tag}_{i}_{step}.png", img)

                # 이미지 객체 생성
                img_sum = tf.image.decode_image(tf.io.read_file(f"D:/CYCLE_GAN/CycleGAN-1/Train_result/{tag}_{i}_{step}.png"), channels=3)
                img_sum = tf.expand_dims(img_sum, 0)  # 배치 차원 추가
                tf.summary.image('%s/%d' % (tag, i), img_sum, step=step)
                img_summaries.append(img_sum)

            self.writer.flush()

    def histo_summary(self, tag, values, step, bins=1000):
        """Log a histogram of the tensor of values."""
        with self.writer.as_default():
            tf.summary.histogram(tag, values, step=step, buckets=bins)
            self.writer.flush()