from flogo.data.dataframe.columns.loaded_image import LoadedImageColumn
from flogo.data.dataframe.readers.image_reader import ImageReader
from flogo.data.dataset.dataset_builder import DatasetBuilder
from flogo.data.dataset.dataset_splitter import DatasetSplitter
from flogo.discovery.training_wrapper import TrainingWrapper
from flogo.discovery.hyperparameters.loss import Loss
from flogo.discovery.hyperparameters.optimizer import Optimizer
from flogo.discovery.model_explorer import ModelExplorer
from flogo.discovery.regularization.early_stopping import EarlyStopping
from flogo.discovery.regularization.monitors.precision_monitor import PrecisionMonitor
from flogo.discovery.tasks.test_task import TestTask
from flogo.discovery.tasks.training_task import TrainingTask
from flogo.preprocessing.mappers.composite import CompositeMapper
from flogo.preprocessing.mappers.leaf.one_hot_mapper import OneHotMapper
from flogo.preprocessing.mappers.leaf.resize_mapper import ResizeMapper
from flogo.preprocessing.mappers.leaf.type_mapper import TypeMapper
from flogo.preprocessing.orchestrator import Orchestrator
from flogo.structure.blocks.convolutional import ConvolutionalBlock
from flogo.structure.blocks.flatten import FlattenBlock
from flogo.structure.blocks.linear import LinearBlock
from flogo.structure.layers.activation import Activation
from flogo.structure.layers.convolutional import Convolutional
from flogo.structure.layers.flatten import Flatten
from flogo.structure.layers.linear import Linear
from flogo.structure.layers.pool import Pool
from flogo.structure.sections.link.flatten import FlattenSection
from flogo.structure.sections.processing.convolutional import ConvolutionalSection
from flogo.structure.sections.processing.feed_forward import LinearSection
from flogo.structure.structure_factory import StructureFactory
from pytorch.architecture.forward import ForwardArchitecture
from pytorch.discovery.hyperparameters.loss import PytorchLoss
from pytorch.discovery.hyperparameters.optimizer import PytorchOptimizer
from pytorch.discovery.measurers.accuracy_measurer import AccuracyMeasurer

from pytorch.discovery.tester import PytorchTester
from pytorch.discovery.trainer import PytorchTrainer
from pytorch.discovery.validator import PytorchValidator
from pytorch.preprocessing.pytorch_caster import PytorchCaster
from pytorch.structure.generator import PytorchGenerator

epochs = 30

path = "C:/Users/Joel/Desktop/mnist"
dataframe = ImageReader().read(path)
dataframe = Orchestrator(OneHotMapper(), CompositeMapper([TypeMapper(LoadedImageColumn), ResizeMapper((28, 28))])) \
    .process(dataframe, ["output"], ["input"])

dataset = DatasetBuilder(PytorchCaster()).build(dataframe, ["input'"], ["output_0", "output_1", "output_2", "output_3",
                                                                        "output_4", "output_5", "output_6", "output_7",
                                                                        "output_8", "output_9"], 5)
train_dataset, test_dataset, validation_dataset = DatasetSplitter().split(dataset)

convolutionalSection = ConvolutionalSection([ConvolutionalBlock([
    Convolutional(1, 6, kernel=3),
    Pool("Max"),
    Activation("ReLU"),
    Convolutional(6, 16, kernel=3),
    Pool("Max"),
    Activation("ReLU")])])

flattenSection = FlattenSection(FlattenBlock(Flatten(1, 3)))

linearSection = LinearSection([LinearBlock([
    Linear(400, 120),
    Activation("ReLU"),
    Linear(120, 10)])])

structure = StructureFactory([convolutionalSection, flattenSection, linearSection],
                             PytorchGenerator()).create_structure()


architecture1 = ForwardArchitecture(structure)
wrapper1 = TrainingWrapper(architecture1,
                           TrainingTask(PytorchTrainer(Optimizer(PytorchOptimizer("SGD", architecture1.parameters(), 0.01)),
                                                       Loss(PytorchLoss("CrossEntropyLoss"))), PytorchValidator(AccuracyMeasurer()),
                                        EarlyStopping(PrecisionMonitor(1))))


convolutionalSection = ConvolutionalSection([ConvolutionalBlock([
    Convolutional(1, 20, kernel=3),
    Pool("Max"),
    Activation("ReLU"),
    Convolutional(20, 50, kernel=3),
    Activation("ReLU"),
    Convolutional(50, 25, kernel=3),
    Pool("Max"),
    Activation("ReLU")
])])

flattenSection = FlattenSection(FlattenBlock(Flatten(1, 3)))

linearSection = LinearSection([LinearBlock([
    Linear(400, 100),
    Activation("ReLU"),
    Linear(100, 10)])])

structure = StructureFactory([convolutionalSection, flattenSection, linearSection],
                             PytorchGenerator()).create_structure()

architecture2 = ForwardArchitecture(structure)
wrapper2 = TrainingWrapper(architecture2,
                           TrainingTask(PytorchTrainer(Optimizer(PytorchOptimizer("SGD", architecture2.parameters(), 0.01)),
                                                       Loss(PytorchLoss("CrossEntropyLoss"))), PytorchValidator(AccuracyMeasurer()),
                                        EarlyStopping(PrecisionMonitor(1))))

convolutionalSection = ConvolutionalSection([ConvolutionalBlock([
    Convolutional(1, 20, kernel=5),
    Pool("Max"),
    Activation("ReLU"),
    Convolutional(20, 50, kernel=3),
    Activation("ReLU"),
    Convolutional(50, 16, kernel=3),
    Pool("Max"),
    Activation("ReLU")
])])

flattenSection = FlattenSection(FlattenBlock(Flatten(1, 3)))

linearSection = LinearSection([LinearBlock([
    Linear(256, 100),
    Activation("ReLU"),
    Linear(100, 25),
    Activation("ReLU"),
    Linear(25, 10)])])

structure = StructureFactory([convolutionalSection, flattenSection, linearSection],
                             PytorchGenerator()).create_structure()

architecture3 = ForwardArchitecture(structure)
wrapper3 = TrainingWrapper(architecture3,
                           TrainingTask(PytorchTrainer(Optimizer(PytorchOptimizer("SGD", architecture3.parameters(), 0.01)),
                                                       Loss(PytorchLoss("CrossEntropyLoss"))), PytorchValidator(AccuracyMeasurer()),
                                        EarlyStopping(PrecisionMonitor(1))))

training_task2 = TrainingTask(PytorchTrainer(Optimizer(PytorchOptimizer("SGD", architecture2.parameters(), 0.01)),
                                    Loss(PytorchLoss("CrossEntropyLoss"))), PytorchValidator(AccuracyMeasurer()),
                     EarlyStopping(PrecisionMonitor(1)))

training_task3 = TrainingTask(PytorchTrainer(Optimizer(PytorchOptimizer("SGD", architecture3.parameters(), 0.01)),
                                    Loss(PytorchLoss("CrossEntropyLoss"))), PytorchValidator(AccuracyMeasurer()),
                     EarlyStopping(PrecisionMonitor(1)))

training_wrappers = [wrapper1, wrapper2, wrapper3]
test_task = TestTask(test_dataset, AccuracyMeasurer(), PytorchTester)
model, accuracy = ModelExplorer(training_wrappers, train_dataset, validation_dataset, test_task).explore(epochs)
print(model)
print(accuracy)