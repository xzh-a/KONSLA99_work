import torch


class ConvBlock(torch.nn.Module):
    def __init__(self, input_size, output_size, kernel_size=3, stride=2, padding=1, activation='relu', batch_norm=True):
        super(ConvBlock, self).__init__()
        self.conv = torch.nn.Conv2d(input_size, output_size, kernel_size, stride, padding) 
        self.batch_norm = batch_norm
        self.bn = torch.nn.InstanceNorm2d(output_size)
        self.activation = activation
        self.relu = torch.nn.ReLU(True) # 음수 값을 0으로 만들어 이미지의 특징을 강조하여 이미지의 핵심 정보를 추출
        self.lrelu = torch.nn.LeakyReLU(0.2, True) # 음수 값을 완전히 제거하지 않고 작은 기울기를 유지하여 학습 안정성을 향상
        self.tanh = torch.nn.Tanh() #  출력 값을 -1 ~ 1 범위로 제한하여 이미지의 특징을 유지하면서 출력 값을 제한하여 이미지의 품질을 향상

    def forward(self, x):
        if self.batch_norm:
            out = self.bn(self.conv(x)) 
        else:
            out = self.conv(x)

        if self.activation == 'relu':
            return self.relu(out)
        elif self.activation == 'lrelu':
            return self.lrelu(out)
        elif self.activation == 'tanh':
            return self.tanh(out)
        elif self.activation == 'no_act':
            return out

# 이미지 업샘플링을 위한 역 convolution 블록
# 업샘플링의 목적: 이미지 해상도 향상, 이미지 블러링 ,  이미지 복원 등등...
# 역conv는 conv의 역 연산을 사용하여 이미지를 확대하는 방법입니다. 
# 컨볼루션은 이미지 크기를 줄이는 작업을 수행하기 때문에, 역 컨볼루션을 사용하여 이미지 크기를 확대. /// 단점 :계산량이 많고,이미지의 품질이 약간 저하될 수 있음.
class DeconvBlock(torch.nn.Module):
    def __init__(self, input_size, output_size, kernel_size=3, stride=2, padding=1, output_padding=1, activation='relu', batch_norm=True):
        super(DeconvBlock, self).__init__()
        self.deconv = torch.nn.ConvTranspose2d(input_size, output_size, kernel_size, stride, padding, output_padding)
        self.batch_norm = batch_norm
        self.bn = torch.nn.InstanceNorm2d(output_size)
        self.activation = activation
        self.relu = torch.nn.ReLU(True)

    def forward(self, x):
        if self.batch_norm:
            out = self.bn(self.deconv(x))
        else:
            out = self.deconv(x)

        if self.activation == 'relu':
            return self.relu(out)
        elif self.activation == 'lrelu':
            return self.lrelu(out)
        elif self.activation == 'tanh':
            return self.tanh(out)
        elif self.activation == 'no_act':
            return out


class ResnetBlock(torch.nn.Module):
    def __init__(self, num_filter, kernel_size=3, stride=1, padding=0):
        super(ResnetBlock, self).__init__()
        conv1 = torch.nn.Conv2d(num_filter, num_filter, kernel_size, stride, padding)
        conv2 = torch.nn.Conv2d(num_filter, num_filter, kernel_size, stride, padding)
        bn = torch.nn.InstanceNorm2d(num_filter)
        relu = torch.nn.ReLU(True)
        pad = torch.nn.ReflectionPad2d(1) #  이미지의 각 차원 (높이, 너비)에 대해 1픽셀씩 패딩을 적용, 이미지 경계 부분의 정보 손실을 방지하고, 특히 컨볼루션 연산과 같은 작업에서 이미지 크기가 변하는 것을 방지

        self.resnet_block = torch.nn.Sequential(
            pad,
            conv1,
            bn,
            relu,
            pad,
            conv2,
            bn
        )

    def forward(self, x):
        out = self.resnet_block(x)
        return out



# network flow :

#입력 이미지에 ReflectionPad2d를 적용하여 패딩을 추가.
#ConvBlock을 통해 이미지의 특징을 추출.
#추출된 특징을 ResNet 블록을 통해  강화.
#DeconvBlock을 통해 출력 이미지를 생성.


# 레이어	 입력 채널	 출력 채널	 역할
# ------------------------------------------------
# Encoder	input_dim	num_filter	이미지 특징 추출
# ------------------------------------------------
# Encoder	num_filter	num_filter * 2	이미지 특징 추출
# ------------------------------------------------
# Encoder	num_filter * 2	num_filter * 4	이미지 특징 추출
# ------------------------------------------------
# ResNet	num_filter * 4	num_filter * 4	이미지 특징 강화
# ------------------------------------------------
# Decoder	num_filter * 4	num_filter * 2	이미지 크기 증가, 채널 감소
# ------------------------------------------------
# Decoder	num_filter * 2	num_filter	이미지 크기 증가, 채널 감소
# ------------------------------------------------
# Decoder	num_filter	output_dim	최종 이미지 생성



class Generator(torch.nn.Module):
    def __init__(self, input_dim, num_filter, output_dim, num_resnet):
        super(Generator, self).__init__()

        # Reflection padding
        self.pad = torch.nn.ReflectionPad2d(3)
        # Encoder -> 3개의 convB 레이어를 통과하면서 특징을 추출 
        self.conv1 = ConvBlock(input_dim, num_filter, kernel_size=7, stride=1, padding=0)
        self.conv2 = ConvBlock(num_filter, num_filter * 2)
        self.conv3 = ConvBlock(num_filter * 2, num_filter * 4)

        # Resnet blocks 
        self.resnet_blocks = []
        for i in range(num_resnet):
            self.resnet_blocks.append(ResnetBlock(num_filter * 4))
        self.resnet_blocks = torch.nn.Sequential(*self.resnet_blocks)

        # Decoder
        self.deconv1 = DeconvBlock(num_filter * 4, num_filter * 2)
        self.deconv2 = DeconvBlock(num_filter * 2, num_filter)
        self.deconv3 = ConvBlock(num_filter, output_dim,
                                 kernel_size=7, stride=1, padding=0, activation='tanh', batch_norm=False) 
        #활성화 함수는 tanh를 사용하여 이미지 픽셀 값을 -1~1 사이로 정규화


    def forward(self, x):
        # Encoder
        enc1 = self.conv1(self.pad(x))
        enc2 = self.conv2(enc1)
        enc3 = self.conv3(enc2)
        # Resnet blocks
        res = self.resnet_blocks(enc3)
        # Decoder
        dec1 = self.deconv1(res)
        dec2 = self.deconv2(dec1)
        out = self.deconv3(self.pad(dec2))
        return out

    # 네트워크 구조상 각 레이어에 적합한 초기화 방법을 사용합니다.
    # 중치는 학습을 통해 최적의 값으로 조정됨, 하지만 초기에 가중치를 무작위로 초기화하지 않으면 학습이 불안정해지거나 성능이 저하될 수 있음. 
    # 따라서 가중치를 적절하게 초기화하는 것은 딥러닝 모델의 성능을 향상시키는 데 중요한 요소.
    def normal_weight_init(self, mean=0.0, std=0.02):
        for m in self.children():
            if isinstance(m, ConvBlock):
                torch.nn.init.normal(m.conv.weight, mean, std)
            if isinstance(m, DeconvBlock):
                torch.nn.init.normal(m.deconv.weight, mean, std)
            if isinstance(m, ResnetBlock):
                torch.nn.init.normal(m.conv.weight, mean, std)
                torch.nn.init.constant(m.conv.bias, 0)



# Discriminator 클래스는 입력 이미지가 실제 이미지인지 생성된 이미지인지를 판별하는 네트워크 구조를 정의. 
# 이 네트워크는 이미지의 특징 추출을 통해 진짜 이미지와 가짜 이미지를 구분합.
class Discriminator(torch.nn.Module):
    def __init__(self, input_dim, num_filter, output_dim):
        super(Discriminator, self).__init__()

        conv1 = ConvBlock(input_dim, num_filter, kernel_size=4, stride=2, padding=1, activation='lrelu', batch_norm=False)
        conv2 = ConvBlock(num_filter, num_filter * 2, kernel_size=4, stride=2, padding=1, activation='lrelu')
        conv3 = ConvBlock(num_filter * 2, num_filter * 4, kernel_size=4, stride=2, padding=1, activation='lrelu')
        conv4 = ConvBlock(num_filter * 4, num_filter * 8, kernel_size=4, stride=1, padding=1, activation='lrelu')
        conv5 = ConvBlock(num_filter * 8, output_dim, kernel_size=4, stride=1, padding=1, activation='no_act', batch_norm=False)

        self.conv_blocks = torch.nn.Sequential(
            conv1,
            conv2,
            conv3,
            conv4,
            conv5
        )

    def forward(self, x):
        out = self.conv_blocks(x)
        return out

    def normal_weight_init(self, mean=0.0, std=0.02):
        for m in self.children():
            if isinstance(m, ConvBlock):
                torch.nn.init.normal(m.conv.weight, mean, std)


    # network flow:
# 입력 이미지를 네트워크에 입력합니다.
# 5개의 ConvBlock 레이어를 순차적으로 통과시켜 이미지의 특징을 추출합니다.
# 마지막 레이어는 활성화 함수를 적용하지 않고, 직접 값을 반환합니다. //  activation='no_act'
# 반환된 값은 이미지가 실제 이미지인지 생성된 이미지인지에 대한 판별 값입니다. 진짜 이미지는 1에 가까운 값을, 가짜 이미지는 0에 가까운 값을 갖습니다.
