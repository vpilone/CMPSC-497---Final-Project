import gradio as gr
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import pdf
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import ollama
import os
import csv
import time


def loadAndRetrieveDocuments(filepath: str) -> Chroma:
    loader = pdf.PyPDFLoader(filepath)
    documents = loader.load()
    textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documentSplits = textSplitter.split_documents(documents)
    embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")
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


filepath = "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/papers/audio-classification/2406.06786v2.pdf"
numReps = 0
directories = [
    "classification",
    "eeg-1",
    "time-series",
    "question-answering",
    "recommendation-systems",
    "openai-gym",
    "visual-navigation",
    "music-generation",
    "visual-odometry",
    "link-prediction",
    "navigate",
    "text-to-image-generation",
    "motion-planning",
    "causal-discovery",
    "graph-learning",
    "atari-games",
    "time-series-forecasting",
    "common-sense-reasoning",
    "audio-classification",
    "language-modelling",
    ".DS_Store",
    "drug-discovery",
    "text-to-sql",
    "decision-making",
    "denoising",
    "music-transcription",
    "visual-reasoning",
    "adversarial-defense",
    "translation",
    "medical-image-segmentation",
    "semantic-segmentation",
    "music-information-retrieval",
    "language-identification",
    "speech-enhancement",
    "image-classification",
    "decoder",
    "transfer-learning",
    "voice-conversion",
    "open-domain-question-answering",
    "reinforcement-learning-1",
    "automatic-speech-recognition",
    "xai",
    "adversarial-robustness",
    "diversity",
    "object-detection",
    "speech-recognition",
    "code-generation",
    "sentence",
    "retrieval",
    "medical-image-analysis",
    "object",
    "computational-efficiency",
    "continuous-control",
    "classification-1",
    "music-source-separation",
    "representation-learning",
    "adversarial-attack",
    "nmt",
    "graph-neural-network",
    "community-question-answering",
    "offline-rl",
    "benchmarking",
    "knowledge-graphs",
    "robot-navigation",
    "machine-learning",
    "dialogue-generation",
    "logical-reasoning",
    "node-classification",
    "speech-synthesis",
    "causal-inference",
    "contrastive-learning",
    "reinforcement-learning",
]

for directory in directories[69:72]:
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
            #             try:
            response = ragChain(
                filepath=filepath,
                question="You have been given an academic research paper in the section labelled “Paper:” that covers a topic related to the development of Artificial Intelligence. Please analyze this paper, and return a response in the format [question, approach] based on the most prevalent artificial intelligence architecture present in the paper. Your response should be in a form usable to train a future AI on the downstream task of creating an AI approach to solve a given research question. Additionally, in your response: question refers to the research question that is trying to be solved by the artificial intelligence architecture, and approach is the architecture used to solve this question. Please be detailed in your response. In particular, when going through the artificial intelligence architecture, please ensure that you mention all required steps for gathering and analyzing the data, as well as each layer the data is then passed through.",
            ).encode("utf-8")
            # response = filepath

            with open(
                "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/fulldatabase.csv",
                "+a",
            ) as csvFile:
                writer = csv.writer(csvFile)
                try:
                    writer.writerow(
                        [filepath, response.split("</think>")[1].encode("utf-8")]
                    )
                except:
                    writer.writerow([filepath, response])
            if numReps < 1:
                numReps += 1
            else:
                numReps = 0
                print(directory + "-" + str(directories.index(directory)))
                time.sleep(180)
                break
# except:
#     print(filepath)

# with open(
#     "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/database.csv",
#     "+r",
# ) as csvFile:
#     reader = csv.reader(csvFile)
#     for row in reader:
#         print(row)
