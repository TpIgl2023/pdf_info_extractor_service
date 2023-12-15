class ExtractText():

    def extractText(self):
        try:
            textDivs = self.dict["text"]["body"]["div"]
            text = ""
            for div in textDivs:
                if "head" in div:
                    text += div["head"] + "\n"
                if "p" in div:
                    paragraphs = div["p"]
                    if isinstance(paragraphs, list):
                        for paragraph in paragraphs:
                            if isinstance(paragraph, dict):
                                if "#text" in paragraph:
                                    text += paragraph["#text"] + "\n"
                            elif isinstance(paragraph, str):
                                text += paragraph + "\n"
                    if isinstance(paragraphs, str):
                        text += paragraphs + "\n"
            self.article.text = text
        except:
            pass
        return self

