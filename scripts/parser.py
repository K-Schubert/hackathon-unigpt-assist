#Parsing the pdf txt files and
def parse_txt(file):
    path = str("../corpus/"+file)
    print(path)
    with open(path) as f:
        doc = f.read().replace('\n','')
    delim = 'Art.'
    splitted =  [delim+e for e in doc.split(delim) if e]
    print(splitted[4])

if __name__ == "__main__":
    parse_txt("RegleGen.txt")