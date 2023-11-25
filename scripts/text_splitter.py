from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(
    separator = "Art\.? | Article\.?",
    chunk_size = 200,
    chunk_overlap = 0,
    length_function = len,
    is_separator_regex = True,
)