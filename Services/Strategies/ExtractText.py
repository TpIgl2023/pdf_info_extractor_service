class ExtractText():

    def extractText(self):
        try:
            textDivs = self.dict["text"]["body"]["div"]
            text = ""
            for div in textDivs:
                if "head" in div:
                    if isinstance(div["head"], dict):
                        if "#text" in div["head"]:
                            text += div["head"]["#text"] + "\n"
                    elif isinstance(div["head"], str):
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
           self.article.text = ""
        return self

