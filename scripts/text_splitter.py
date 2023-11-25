from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(
    separator = "Art\.",
    chunk_size = 2000,
    chunk_overlap = 200,
    length_function = len,
    is_separator_regex = True,
)