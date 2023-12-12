from abc import ABC , abstractmethod

class ExtractAuthors(ABC):
    @abstractmethod
    def extractAuthors(self):
        pass