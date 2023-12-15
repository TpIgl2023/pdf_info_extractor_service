from Services.Strategies.ExtractAuthors import ExtractAuthors


class ExtractInstitutions():
    @staticmethod
    def extract_affiliations(authors):
        affiliations = set()
        if isinstance(authors, dict):
            myAffiliations = ExtractAuthors.extract_affiliation_from_author(authors)
            if myAffiliations != None:
                affiliations.add(myAffiliations)
        elif isinstance(authors, list):
            for author in authors:
                myAffiliations = ExtractAuthors.extract_affiliation_from_author(author)
                if myAffiliations != None:
                    affiliations.add(myAffiliations)
        affiliations.discard("N/A")
        if len(affiliations) == 0:
            return None
        return list(affiliations)

    def extractInstitutions(self):
        try:
            authors = self.dict['teiHeader']['fileDesc']['sourceDesc']['biblStruct']['analytic']['author']
            affiliations = self.extract_affiliations(authors)
            self.article.institutions = affiliations
        except:
            pass
        return self