from vocabulary import Channel, Activation
from model.architecture.layers import Linear, ActivationFunction


class FeedForward:
    def __init__(self, architecture):
        self.architecture = [LinearBlock(block) for block in architecture]

    def pytorch(self):
        result = []
        for block in self.architecture: result.extend(block.pytorch())
        return result


class LinearBlock:
    def __init__(self, block):
        self.linear = Linear(block[Channel.In], block[Channel.Out])
        self.activation = ActivationFunction(block[Activation.name])

    def pytorch(self):
        return self.linear.pytorch(), self.activation.pytorch()
