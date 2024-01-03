class ExtractAbstract():
    def extractAbstract(self):
        try:
            if self.dict['teiHeader']['profileDesc']['abstract'] != None:
                self.article.abstract = self.dict['teiHeader']['profileDesc']['abstract']['div']['p']

        except:
            self.article.abstract = None
        return self