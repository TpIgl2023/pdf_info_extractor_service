from abc import ABC , abstractmethod

class ExtractText(ABC):
    @abstractmethod
    def extractText(self):
        pass
