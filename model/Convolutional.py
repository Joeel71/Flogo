from torch import nn
from torch.nn import MaxPool2d, Conv2d


class ConvolutionalArchitecture:
    def __init__(self, architecture):
        self.architecture = [ConvolutionalBlock(block) for block in architecture]

    def pytorch(self):
        result = []
        for block in self.architecture: result.extend(block.pytorch())
        return result


class ConvolutionalBlock:
    def __init__(self, block):
        self.convolutional_layer = Conv(block["kernel_conv"],
                                        block["in_channels"],
                                        block["out_channels"])
        self.activation_function = Activation(block["activation"])
        self.pool_layer = Pool(block["kernel_pool"],
                               block["stride"],
                               block["padding"])

    def pytorch(self):
        return self.convolutional_layer.pytorch(), self.activation_function.pytorch(), self.pool_layer.pytorch()


class Conv:
    def __init__(self, kernel_size, in_channels, out_channels):
        self.kernel_size = kernel_size
        self.in_channels = in_channels
        self.out_channels = out_channels

    def pytorch(self):
        return Conv2d(kernel_size=self.kernel_size, in_channels=self.in_channels, out_channels=self.out_channels)


class Pool:
    def __init__(self, pool, stride, padding):
        self.kernel = pool
        self.stride = stride
        self.padding = padding

    def pytorch(self):
        return MaxPool2d(kernel_size=self.kernel, stride=self.stride, padding=self.padding)


class Activation:
    def __init__(self, name):
        self.name = name

    def pytorch(self):
        return getattr(nn, self.name)()
