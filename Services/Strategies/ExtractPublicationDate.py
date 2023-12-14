import json
from datetime import datetime

class ExtractPublicationDate():
    @staticmethod
    def format_date(input_date):
        # Ajoutez le jour et le mois par défaut si seulement l'année est fournie
        if len(input_date) == 4:
            input_date += "-01-01"
        elif len(input_date) == 7:
            input_date += "-01"

        # Essayez de convertir la chaîne en objet datetime
        try:
            formatted_date = datetime.strptime(input_date, "%Y-%m-%d")
            return formatted_date
        except ValueError:
            print("Format de date invalide. Utilisation du format par défaut.")
            return None
    def extractPublicationDate(self):
        try:
            filedesc = self.dict['teiHeader']['fileDesc']
            dateJSON = None
            if 'publicationStmt' in filedesc:
                if 'publisher' in filedesc['publicationStmt']:
                    publisher = filedesc['publicationStmt']
                    if 'date' in publisher:
                        date = publisher['date']['@when']
                        formatted_date = ExtractPublicationDate.format_date(date)
                        dateJSON = json.dumps({"formatted_date": formatted_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[
                                                                 :-3] + "Z"} if formatted_date else None)
            self.article.publishingDate = dateJSON
        except:
            pass
        return self