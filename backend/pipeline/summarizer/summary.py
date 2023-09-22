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

    chunk_sum_template = """
    You will be given a part of section transript from a podcast. 
    The section will be enclosed in triple backticks (```)
    Your goal is to give a summary of this section with domain knowledge of \
    professional neuroscience so that a reader will have a full understanding of what this \
    section of podcast is about.
    Your response should be at leat three paragraphs and fully encompasses what was \
    said in the part of podcast.

    SECTION OF TRANSCRIPT: ```{text}```

    FULL SUMMARY: 
    """

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
    with open("summary-list.txt", "a", encoding='utf-8') as f:
        for i, summary in enumerate(summary_list, start=1):
            formatted_sum = f"Summary #{i} (chunk #{selected_chunk_indices[i-1]}) - Preview: {summary}\n\n"
            f.write(formatted_sum)

    return summary_list


def get_final_summary(summary_list):
    # Join the summaries as a whole paragraphs
    summaries = "\n\n".join(summary_list)
    
    # Convert it back to a document
    summaries = Document(page_content=summaries)

    final_sum_template = """
    You are a professional neuroscientist and very capable of giving reader \
    great insights from neuroscience articles.

    You are about to be given a series of summaries wrapped in triple backticks from a neuroscience podcast by Andrew Huberman.
    Your goal is to give an insightful summary from those combined chunk of summaries, \
    so that the reader should be able to learn the essence and salient points from this podcast.
    Your response should be at leat three paragraphs and fully encompass what was said in those summaries.

    SERIES OF SUMMARIES: ```{text}```

    INSIGHTFUL SUMMARY:
    """

    final_sum_prompt = PromptTemplate(template=final_sum_template, input_variables=["text"])

    final_sum_chain = load_summarize_chain(
        llm=advanced_summary_model,
        prompt=final_sum_prompt,
        chain_type="stuff",
        verbose=True
    )

    final_summary =final_sum_chain.run([summaries])

    return final_summary


# Bring them all together
def start_summarize(text):
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
    final_summary = get_final_summary(summary_list)

    print("Saving final summary into text file...")
    print()
    with open("huberman_summary.txt", "w", encoding='utf-8') as f:
        f.write(final_summary)

    return final_summary
    

if __name__ == "__main__":
    start = time.time()
    with open("huberman_transcript.txt", "r", encoding='utf-8') as f:
        transcript = f.read()

    final_summary = start_summarize(transcript)
    end = time.time()

    time_spent = end - start
    print(f"Time total time spent: {time_spent} seconds")