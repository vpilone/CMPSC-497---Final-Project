import gradio as gr
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import pdf
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import ollama
import os
import csv


def loadAndRetrieveDocuments(filepath: str) -> Chroma:
    loader = pdf.PyPDFLoader(filepath)
    documents = loader.load()
    textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documentSplits = textSplitter.split_documents(documents)
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vectorStore = Chroma.from_documents(documents=documentSplits, embedding=embeddings)
    return vectorStore.as_retriever()


def formatDocuments(documents: list) -> str:
    return "\n\n".join(document.page_content for document in documents)


def ragChain(filepath: str, question: str) -> str:
    retriever = loadAndRetrieveDocuments(filepath)
    retrievedDocs = retriever.invoke(question)
    formattedContext = formatDocuments(retrievedDocs)
    formattedPrompt = f"{question}\n\nPaper: {formattedContext}"
    response = ollama.chat(
        model="qwq", messages=[{"role": "user", "content": formattedPrompt}]
    )
    return response["message"]["content"]


filepath = "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/papers/machine-learning/1603.02754v3.pdf"
# response = ragChain(
#     filepath,
#     "You have been given an academic research paper in the section labelled “Paper:” that covers a topic related to the development of Artificial Intelligence. Please analyze this paper, and return a response in the list format [question, approach] based on the most prevalent artificial intelligence architecture  present in the paper. In your response: question refers to the research question that is trying to be solved by the artificial intelligence architecture, and approach is the architecture used to solve this question. Please be detailed in your response. In particular, when going through the artificial intelligence architecture, please ensure that you mention all required steps for gathering and analyzing the data, as well as each layer the data is then passed through.",
# )

# response = "testing\ntesting,\n123".encode("utf-8")

# try:
#     response1 = response.split("**Question:**")[1]
#     response2 = response1.split("**Approach:**")
#     print(response2)
# except:
#     print("error")

# questionResponse = ragChain(
#     filepath,
#     "You have been given an academic research paper in the section labelled “Paper:” that covers a topic related to the development of Artificial Intelligence. Please analyze this paper, and return the research question that the paper was attempting to answer based on the most prevalent artificial intelligence architecture present in the paper. Specifically, the question refers to the research question that is trying to be solved by the artificial intelligence architecture.Please be detailed in your response.",
# )

# answerResponse = ragChain(
#     filepath,
#     "You have been given an academic research paper in the section labelled “Paper:” that covers a topic related to the development of Artificial Intelligence. Please analyze this paper, and return an approach based on the most prevalent artificial intelligence architecture  present in the paper. Specifically, approach is the architecture used to solve the research question prevalent in the paper. Please be detailed in your response. In particular, when going through the artificial intelligence architecture, please ensure that you mention all required steps for gathering and analyzing the data, as well as each layer the data is then passed through.",
# )

for directory in os.listdir(
    "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/papers"
):
    if directory != ".DS_Store":
        for file in os.listdir(
            "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/papers/"
            + directory
        ):
            filepath = (
                "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/papers/"
                + directory
                + "/"
                + file
            )

            response = ragChain(
                filepath=filepath,
                question="You have been given an academic research paper in the section labelled “Paper:” that covers a topic related to the development of Artificial Intelligence. Please analyze this paper, and return a response in the format [question, approach] based on the most prevalent artificial intelligence architecture present in the paper. Your response should be in a form usable to train a future AI on the downstream task of creating an AI approach to solve a given research question. Additionally, in your response: question refers to the research question that is trying to be solved by the artificial intelligence architecture, and approach is the architecture used to solve this question. Please be detailed in your response. In particular, when going through the artificial intelligence architecture, please ensure that you mention all required steps for gathering and analyzing the data, as well as each layer the data is then passed through.",
            ).encode("utf-8")

            with open(
                "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/database.csv",
                "+a",
            ) as csvFile:
                writer = csv.writer(csvFile)
                try:
                    writer.writerow(
                        [filepath, response.split("</think>")[1].encode("utf-8")]
                    )
                except:
                    writer.writerow([filepath, response])


# with open(
#     "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/database.csv",
#     "+r",
# ) as csvFile:
#     reader = csv.reader(csvFile)
#     for row in reader:
#         print(row)
