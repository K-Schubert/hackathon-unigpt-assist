import json
from pdf_2_text import extraire_texte_pdf
from text_splitter import text_splitter

PATH_LIB = "./corpus/library.json"
CORPUS_PATH = "./corpus/"
PREPROCESSED_PATH = "./pre-processed/unige.jsonl"

class DocumentUnige:
    def __init__(self, title, src, url=""):
        self.title = title
        self.url = url
        self.src = src

    def get_text(self):
        if self.src.endswith(".txt"):
            with open(CORPUS_PATH + self.src, 'r') as infile:
                text = infile.read()
        elif self.src.endswith(".pdf"):
            text = extraire_texte_pdf(CORPUS_PATH + self.src)
        else:
            raise Exception("Format de fichier non supporté")
        return text

    def get_langchain_docs(self):
        lang_docs = text_splitter.create_documents([self.get_text()])
        lang_docs = [doc for doc in lang_docs if len(doc.page_content) < 4000]
        for doc in lang_docs:
            doc.metadata["title"] = self.title
            doc.metadata["url"] = self.url
        self.write_corpus_doc_debug(lang_docs)  # FOR DEBUGGING PURPOSES REMOVE LATER
        return lang_docs

    def to_json(self):
        return json.dumps(self.__dict__)
    
    def write_corpus_doc_debug(self, lang_docs):
        splitted_txt = ""
        for i, text in enumerate(lang_docs):
            # Ensure that 'text' here is a list of tokens. If it's a string, this will count characters.
            print('Document #{}: {} tokens'.format(i, len(text.page_content)))
            splitted_txt += text.page_content + "\n" +"*"*100 + "\n"

        with open(CORPUS_PATH + self.src.split(".")[0] + "_splitted.txt", 'w') as f:
            f.write(splitted_txt)


class LibraryUnige:
    def __init__(self):
        self.documents = []
        self.retrieve_json()

    def add_document(self, title, src, url=""):
        new_document = DocumentUnige(title, src, url)
        self.documents.append(new_document)

    def library_to_json(self):
        return json.dumps([doc.to_json() for doc in self.documents], indent=4)

    def write_json(self, path):
        with open(path, 'w') as outfile:
            json.dump(self.library_to_json(), outfile, indent=4, ensure_ascii=False)

    def retrieve_json(self):
        with open(PATH_LIB, 'r') as infile:
            data = json.load(infile)
        for doc in data:
            self.add_document(doc["title"], doc["src"], doc["url"])

    def get_langchain_docs(self):
        lang_docs = []
        for doc in self.documents:
            lang_docs += doc.get_langchain_docs()
        return lang_docs
    
    def save_langchain_docs(self):
        lang_docs = self.get_langchain_docs()
        # save to jsonl
        docs_to_save = []
        for doc in lang_docs:
            docs_to_save.append({"content": doc.page_content, "metadata": doc.metadata})

        with open(PREPROCESSED_PATH, 'w') as f:
            for item in docs_to_save:
                f.write(json.dumps(item) + "\n")
    
if __name__ == "__main__":
    lib = LibraryUnige()
    lib.save_langchain_docs()