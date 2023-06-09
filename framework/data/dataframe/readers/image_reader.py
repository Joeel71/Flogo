from os import listdir
from os.path import join

from framework.data.dataframe.columns.categorical import CategoricalColumn
from framework.data.dataframe.columns.unloaded_image import UnloadedImageColumn
from framework.data.dataframe.dataframe import Dataframe


class ImageReader:

    def read(self, path):
        images, labels = [], []
        for directory in listdir(path):
            self.__extract_images_from(path, directory, images, labels)
        return Dataframe({"input": UnloadedImageColumn(images), "output": CategoricalColumn(labels)})

    def __extract_images_from(self, path, directory, images, labels):
        for image_name in listdir(join(path, directory)):
            images.append(join(path, directory, image_name))
            labels.append(directory)
