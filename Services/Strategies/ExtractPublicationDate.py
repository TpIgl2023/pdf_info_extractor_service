from abc import ABC , abstractmethod

class ExtractPublicationDate(ABC):
    @abstractmethod
    def extractPublicationDate(self):
        pass