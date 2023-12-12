from abc import ABC

# Interface pour la stratégie d'extraction d'objet
class DictExtractionStrategy(ABC):
    def extractDict(self, article_data):
        pass