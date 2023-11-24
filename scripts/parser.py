import re
#Parsing the pdf txt files and
def parse_txt(file):
    path = str("../corpus/"+file)
    print(path)
    with open(path) as f:
        doc = f.read().replace('\n','')

    
    # Use regular expression to find all occurrences of "Art. x" followed by any text
    pattern = re.compile(r'^Art\. +[0-z]', re.DOTALL)

    # Extract all matches into a list
    result = pattern.findall(doc)


    print(result)

if __name__ == "__main__":
    parse_txt("RegleGen.txt")