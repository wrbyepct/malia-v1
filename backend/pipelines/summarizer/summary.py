#Loader
from langchain.schema import Document

# Splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Embedding Support
from langchain.embeddings import OpenAIEmbeddings

# Prompt template
from langchain.prompts import PromptTemplate

# Summarizer, use for map reduce
from langchain.chains.summarize import load_summarize_chain

# Data Science
from sklearn.cluster import KMeans
import numpy as np

# Other tools
import time

# My own modules
from agent.models import chuck_summary_model, advanced_summary_model

# summary templates
from utils.template import CHUNK_SUMMARY_TEMPLATE, FULL_SUMMARY_TEMPLATE
from utils.config import (
    SHORT_FULL_SUMMARY_FILE_PATH, 
    LONG_FULL_SUMMARY_FILE_PATH,
    CHOSEN_DOCS_SUMMARY_LIST_PATH
)

# First split the documents
def split_text_to_docs(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '\t'],
        chunk_size=2000,
        chunk_overlap=400
    )
    docs = text_splitter.create_documents([text])
    return docs

# Store them as vectors
def store_as_vectors(docs):
    embeddings = OpenAIEmbeddings()
    vectors = embeddings.embed_documents([d.page_content for d in docs])
    return vectors

# Select the most representitive ones
# The one that's the closest to centroid
def select_closest_chunks(vectors):
    # Find the clusters among those vector docs
    n_clusters = 10
    kmeans = KMeans(n_init='auto', n_clusters=n_clusters, random_state=42).fit(vectors)

    closest_indices = []
    for i in range(n_clusters):
        # Get the list of distances from that particular cluster center
        distances = np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1)

        # Find the list position of closest one (using argmin to find the smallest distance)
        # The postion is also the location of the split documents in terms of order
        closest_index = np.argmin(distances)

        closest_indices.append(closest_index)
    
    # Sort the doucment places, so that we start from 1
    selected_indices = sorted(closest_indices)
    
    return selected_indices


def summarize_each_chunk(docs, selected_chunk_indices):

    chunk_sum_template = CHUNK_SUMMARY_TEMPLATE

    chunk_sum_prompt = PromptTemplate(template=chunk_sum_template, input_variables=['text'])

    # Use summarize chain to do the work
    chunk_sum_chain = load_summarize_chain(
        llm=chuck_summary_model,
        prompt=chunk_sum_prompt,
        chain_type="stuff"
    )

    # Select the chucks in our selected indicies
    selected_docs = [docs[i] for i in selected_chunk_indices]   

    # Summarize every chunk
    summary_list = []
    for i, doc in enumerate(selected_docs, start=1):
        chunk_summary = chunk_sum_chain.run([doc])
        summary_list.append(chunk_summary)
    
    # For exmamination purpose
    print("Saving each chunk into text file...")
    print()
    with open(CHOSEN_DOCS_SUMMARY_LIST_PATH, "w+", encoding='utf-8') as f:
        for i, summary in enumerate(summary_list, start=1):
            formatted_sum = f"Summary #{i} (chunk #{selected_chunk_indices[i-1]}) - Preview: {summary}\n\n"
            f.write(formatted_sum)

    return summary_list


def get_final_summary(summary_list, title, url, channel_name):
    # Join the summaries as a whole paragraphs
    summaries = "\n\n".join(summary_list)
    
    print("Saving long full summary into text file...")
    print()
    with open(LONG_FULL_SUMMARY_FILE_PATH, "w", encoding='utf-8') as f:
        f.write(summaries)
    
    # Convert it back to a document
    summaries = Document(page_content=summaries)

    final_sum_template = FULL_SUMMARY_TEMPLATE

    final_sum_prompt = PromptTemplate(template=final_sum_template, input_variables=["text"])

    final_sum_chain = load_summarize_chain(
        llm=advanced_summary_model,
        prompt=final_sum_prompt,
        chain_type="stuff",
        verbose=True
    )

    final_summary = final_sum_chain.run([summaries])
    
    # Save as detailed info for later tweets generation
    video_info = f"""Useful info for the video: {title}
VIDEO TITLE: {title}
VIDEO LINK: {url}
VIDEO CHANNEL NAME: {channel_name}

VIDEO FULl SMMARY: {final_summary}    
"""
    print("Final summary done!")
    print()
    print("Saving final summary into text file...")
    print()
    with open(SHORT_FULL_SUMMARY_FILE_PATH, "w", encoding='utf-8') as f:
        f.write(video_info)
    return final_summary


# Bring them all together
def start_summarize(text, title, url, channel_name):
    print("Splitting text into documents...")
    print()
    docs = split_text_to_docs(text)

    print("Embedding into vectors...")
    print()
    vectors = store_as_vectors(docs)

    print("Finding the closest chunks...")
    print()
    selected_chunk_indices = select_closest_chunks(vectors)

    print("Summarizing each chunk...")
    print()
    summary_list = summarize_each_chunk(docs=docs, selected_chunk_indices=selected_chunk_indices)

    print("Summarizing final summary...")
    print()
    final_summary = get_final_summary(
        summary_list=summary_list, 
        title=title, 
        url=url, 
        channel_name=channel_name
    )

    return final_summary
    

if __name__ == "__main__":
    start = time.time()
    with open("huberman_transcript.txt", "r", encoding='utf-8') as f:
        transcript = f.read()

    final_summary = start_summarize(transcript)
    end = time.time()

    time_spent = end - start
    print(f"Time total time spent: {time_spent} seconds")