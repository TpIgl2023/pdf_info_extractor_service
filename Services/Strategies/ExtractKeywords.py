from abc import ABC , abstractmethod

class ExtractKeywords(ABC):
    @abstractmethod
    def extractKeywords(self):
        pass