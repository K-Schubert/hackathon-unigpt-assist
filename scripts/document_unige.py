import json

class DocumentUnige:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def to_json(self):
        return json.dumps(self.__dict__)

# Example usage
document = DocumentUnige("My Document", "John Doe")
json_data = document.to_json()
print(json_data)
