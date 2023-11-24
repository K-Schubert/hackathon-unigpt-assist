from pdf_2_text import extraire_texte_pdf, nettoyer_texte
from text_splitter import text_splitter
import json

if __name__ == '__main__':
    chemin_pdf = './corpus/RegleGen.pdf'
    texte_brut = extraire_texte_pdf(chemin_pdf)

    # Write to a file
    with open('./corpus/RegleGen.txt', 'w') as f:
        f.write(texte_brut)

    # Assuming text_splitter.create_documents returns a list of tokenized documents
    texts = text_splitter.create_documents([texte_brut])
    
    # Optionally print the first document (if it's large, consider printing just a part of it)
    # print(texts[0])
        # Iterate over the documents and print the number of tokens in each

    splitted_txt = ""
    for i, text in enumerate(texts):
        # Ensure that 'text' here is a list of tokens. If it's a string, this will count characters.
        print('Document #{}: {} tokens'.format(i, len(text.page_content)))
        splitted_txt += text.page_content + "\n" +"*"*100 + "\n"

    with open('./corpus/RegleGen_splitted.txt', 'w') as f:
        f.write(splitted_txt)

    # save to jsonl
    docs_to_save = []
    for doc in texts:
        docs_to_save.append({"content": doc.page_content, "metadata": doc.metadata})
        # add metadata to the document
        doc.metadata["url"] = "https://www.unige.ch/sciences/files/2115/3745/7266/RegleGen.pdf"
        doc.metadata["title"] = "Règlement d'études de la Faculté des sciences"
        doc.metadata["author"] = "Faculté des sciences"

    with open("./pre-processed/RegleGen.json", 'w') as f:
        for item in docs_to_save:
            f.write(json.dumps(item) + "\n")

    # write a 