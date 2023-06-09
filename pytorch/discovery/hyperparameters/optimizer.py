from torch import optim


class PytorchOptimizer:
    def __init__(self, name, model_params, lr):
        self.optimizer = self.__build(name, model_params, lr)
        self.optimizer.zero_grad()

    def __build(self, name, model_params, lr):
        return getattr(optim, name)(model_params, lr)

    def step(self):
        self.optimizer.step()
        self.optimizer.zero_grad()
