
class ExtractKeywords():
    def extractKeywords(self):
        try:
            keywords = self.dict['teiHeader']['profileDesc']['textClass']['keywords']['term']
            self.article.keywords = keywords
        except:
            pass
        return self