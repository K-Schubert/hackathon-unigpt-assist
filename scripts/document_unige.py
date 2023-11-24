import json

class DocumentUnige:
    def __init__(self, title, author, src, url=""):
        self.title = title
        self.author = author
        self.url = url
        self.src = src

    def to_json(self):
        return json.dumps(self.__dict__)


class LibraryUnige:
    def __init__(self):
        self.documents = []

    def add_document(self, title, author, src, url=""):
        new_document = DocumentUnige(title, author, src, url)
        self.documents.append(new_document)

    def library_to_json(self):
        return json.dumps([doc.to_json() for doc in self.documents], indent=4)

if __name__ == "__main__":
    # Example of use
    # Exemple d'utilisation
    library = LibraryUnige()
    library.add_document("Titre 1", "Auteur 1", "Source 1", "URL 1")
    library.add_document("Titre 2", "Auteur 2", "Source 2")

    # Convertir la bibliothèque en JSON
    json_library = library.library_to_json()
    # write json to file
    with open('./corpus/library.json', 'w') as outfile:
        json.dump(json_library, outfile)
