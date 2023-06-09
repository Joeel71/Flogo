import torch.nn

import framework.structure.layers.normalization


class PNormalization:
    def __init__(self, norm: framework.structure.layers.normalization.Normalization):
        self.out_channels = norm.out_channels
        self.momentum = norm.momentum
        self.eps = norm.eps

    def build(self):
        return torch.nn.BatchNorm2d(self.out_channels, eps=self.eps, momentum=self.momentum)
