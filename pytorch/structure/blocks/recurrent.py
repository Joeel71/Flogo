from flogo.structure.blocks import recurrent
from pytorch.structure.sections.processing.recurrent.recurrent_pytorch_units import LSTMCell, RNNCell, GRUCell


class RecurrentBlock:
    def __init__(self, block: recurrent.RecurrentBlock):
        self.channel_in = block.channel_in
        self.channel_out = block.channel_out
        self.block_type = block.type_
        self.activation = block.activation_name
        self.bias = block.bias

    def build(self):
        if self.block_type == "LSTMCell": return LSTMCell(self.channel_in, self.channel_out, self.bias)
        if self.block_type == "RNNCell": return RNNCell(self.channel_in, self.channel_out, self.bias, self.activation)
        if self.block_type == "GRUCell": return GRUCell(self.channel_in, self.channel_out, self.bias)