class ExtractTitle():
    def extractTitle(self):
        try:
            self.article.title = self.dict['teiHeader']['fileDesc']['titleStmt']['title']['#text']
        except:
            pass
        return self
