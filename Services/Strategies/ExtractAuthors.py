class ExtractAuthors():
    @staticmethod
    def handleAuthorsArray(authors):
        authors_cleaned = []
        if isinstance(authors, list):
            for author in authors:
                authors_cleaned.append(ExtractAuthors.extract_full_name(author))
            return authors_cleaned
        return [ExtractAuthors.extract_full_name(authors)]
    @staticmethod
    def extract_full_name(data):
        if "persName" not in data:
            return ""
        if 'surname' in data['persName']:
            last_name = data['persName']['surname']
        else:
            last_name = ""
        if 'forename' in data['persName']:
            if isinstance(data['persName']['forename'], list):
                first_name = data['persName']['forename'][0]['#text']
                first_name += " " + data['persName']['forename'][1]['#text']
            else:
                first_name = data['persName']['forename']['#text']
        else:
            first_name = ""

        return f"{last_name} {first_name}"

    @staticmethod
    def extract_affiliation_from_author(author):
        if 'affiliation' in author:
            affiliation_info = author['affiliation']
            if 'orgName' in affiliation_info:
                orgArray = affiliation_info['orgName']
                org_name = ""
                if isinstance(orgArray, list):
                    org_name = orgArray[0]['#text']
                elif isinstance(orgArray, dict):
                    org_name = orgArray['#text']
            else:
                org_name = "N/A"

            if isinstance(affiliation_info, list):
                affiliation_info = affiliation_info[0]

            address_info = affiliation_info.get('address', {})
            post_code = address_info.get('postCode', "N/A")
            country = address_info.get('country', {}).get('#text', "N/A")

            if (org_name == "N/A" and post_code == "N/A" and country == "N/A"):
                return None

            myString = str(org_name + ", " + post_code + ", " + country)

            return myString
        myString = "N/A"
        return myString

    def extractAuthors(self):
        try:
            authors = self.dict['teiHeader']['fileDesc']['sourceDesc']['biblStruct']['analytic']['author']
            self.article.authors = self.handleAuthorsArray(authors)
        except:
            self.article.authors = []
        return self