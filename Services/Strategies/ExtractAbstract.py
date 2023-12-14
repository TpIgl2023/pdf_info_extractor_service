class ExtractAbstract():
    def extractAbstract(self):
            if self.dict['teiHeader']['profileDesc']['abstract'] != None:
                self.article.abstract = self.dict['teiHeader']['profileDesc']['abstract']['div']['p']
            return self