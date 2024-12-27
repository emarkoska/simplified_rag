import os.path
from os import listdir
from dotenv import load_dotenv
from os.path import isfile, join
from typing import Literal, get_args
from langchain.chains import RetrievalQA
from langchain.schema.document import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import DocArrayInMemorySearch

DataSource = Literal["Nov 2024 MPC Report"]
SUPPORTED_DATA_SOURCES = get_args(DataSource)

# loading API keys from env
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if OPENAI_API_KEY == 'xxxxxxxx':
    raise ValueError("Please add your own OpenAI API key in the .env file by replacing 'xxxxxxxx' with your own key.")

# loading model and defining embedding
llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')
embeddings = OpenAIEmbeddings()

# get target folder for uploaded docs
target_folder = "./docs/"

def load_data_set(source: DataSource, query: str):
    if source not in SUPPORTED_DATA_SOURCES:
        raise ValueError(f"Provided data source {source} is not supported.")

    # fragmenting the document content to fit in the number of token limitations
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)

    # get files from target directory
    my_file = [f for f in listdir(target_folder) if isfile(join(target_folder, f))]
    my_file = target_folder + my_file[0]
    print(f"my file is {my_file}")

    # load uploaded pdf file
    loader = PyPDFLoader(my_file)
    data = loader.load()
    split_docs = text_splitter.split_documents(data)

    data_set = DocArrayInMemorySearch.from_documents(documents = split_docs, embedding = embeddings)

    return data_set


def retrieve_info(source: DataSource, data_set: DocArrayInMemorySearch, query: str):
    if source not in SUPPORTED_DATA_SOURCES:
        raise ValueError(f"Provided data source {source} is not supported.")

    qa = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type="stuff",
        retriever = data_set.as_retriever(), # repla
        verbose=True,
    )

    preface = "Pretend you're representing the MPC at the Bank of England and you're being asked questions at a press conference" \
              "for the November 2024 monetary policy report which cut rates down to 4.75%. You can't say that you don't know or you don't have the" \
              " information. You're an MPC member and you must provide an answer, use the document and your knowledge of economics" \
              "to do this. You must also ensure that you're politically-neutral, and look after the reputation of the Bank of" \
              " England. Give a 2-3 paragraph answer. Answer the following question with the information available to you: "
    query = preface + query

    output = qa.invoke(query)

    return output


def generate_answer(selection: DataSource, query: str):
    if selection not in SUPPORTED_DATA_SOURCES:
        raise ValueError(f"Provided data source {selection} is not supported.")

    data_set = load_data_set(selection, query)
    response = retrieve_info(selection, data_set, query)
    
    return response