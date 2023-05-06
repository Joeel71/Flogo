from flogo.preprocessing.column import Column
from flogo.preprocessing.mapper import Mapper


class CompositeMapper(Mapper):
    def __init__(self, mappers: list()):
        self.mappers = mappers if len(mappers) != 0 else []

    def apply(self, column: Column):
        for mapper in self.mappers:
            column = mapper.apply(column)
        return column
