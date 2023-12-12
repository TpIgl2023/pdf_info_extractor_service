from abc import ABC , abstractmethod

class ExtractTitle(ABC):
    @abstractmethod
    def extractTitle(self):
        pass