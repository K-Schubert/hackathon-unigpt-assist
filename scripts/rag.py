import pandas as pd

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

import pinecone
from langchain.vectorstores import Pinecone

import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
PINECONE_INDEX = os.getenv('PINECONE_INDEX')

def init_pinecone():

    # init pinecone index
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT,
    )

    if PINECONE_INDEX not in pinecone.list_indexes():
        pinecone.create_index(PINECONE_INDEX, dimension=1536, metric="cosine")

    index = pinecone.Index(PINECONE_INDEX)

    return index

def init_vectorstore():

    # init embedding function
    embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002",
                                disallowed_special=())

    vectorstore = Pinecone.from_existing_index(
                index_name=PINECONE_INDEX,
                embedding=embedding_function,
                #namespace=namespace
                )
    
    return vectorstore

def init_retriever(k):

    # init retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": k}, return_source_documents=True)

    return retriever

def init_retrievalqa_chain():

    index = init_pinecone()
    vectorstore = init_vectorstore()
    retriever = init_retriever(k=10)

    # init llm
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,
                    model="gpt-4-1106-preview",
                    temperature=0)

    # init prompt template
    template = """
            Vous êtes un assistant qui répond à des questions sur l'Université de Genève, basée en Suisse.
            Utilisez les éléments de contexte et l'historique du chat suivants pour répondre aux questions. 
            Votre réponse doit être liée à l'Université de Genève uniquement. Si la question ne figure pas dans le contexte ou l'historique du chat, répondez "Je suis désolé, je ne connais pas la réponse".
            Les réponses doivent être détaillées mais concises et courtes.
            Respirez profondément et travaillez étape par étape.
            
            Context: {context}

            Question: {question}
            Answer: """

    prompt = PromptTemplate(input_variables=["context", "question"], template=template)

    # init retrievalQA chain
    qa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": prompt},
                return_source_documents=True
                )
    
    return qa

def run_query(qa, query):

    res = qa({"query": query})

    return {"answer": res["result"], "source_documents": res["source_documents"]}

if __name__ == "__main__":

    qa = init_retrievalqa_chain()

    answer, source_documents = run_query(qa, query)