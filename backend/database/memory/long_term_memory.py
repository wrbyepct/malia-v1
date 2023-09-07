from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
import os
from utils.tools import INFORMATION_ABOUT_JAY
import shutil

# For deleting vdb
from utils.config import VDB_DIR
import os


# Load from vdb and create vector store memory
class VDB:
    def __init__(self):
        if os.path.exists(VDB_DIR):
            # If long memory exists, directly use it
            self.vdb = Chroma(persist_directory=VDB_DIR, embedding_function=OpenAIEmbeddings())
        else:
            # Else create a new one with primed knowledge
            vdb.vdb = Chroma.from_texts(INFORMATION_ABOUT_JAY, persist_directory=VDB_DIR, embedding=OpenAIEmbeddings())
        self.retriever = self.vdb.as_retriever(search_kwargs=dict(k=5))
        self.v_memory = VectorStoreRetrieverMemory(retriever=self.retriever)



def save_to_vdb(dialogues, message_time):
    # Save the recent 2 messages to vdb
    [jay, malia] = dialogues
    [jay_time, malia_time] = message_time
    
    jay_message = f"""Jay: {jay}
Time of Record: {jay_time}
"""
    malia_message = f"""MALIA: {malia}
Time of Record: {malia_time}
"""

    try: 
        vdb.vdb.add_texts([jay_message, malia_message])
        vdb.vdb.persist()
        print("###Recent chat saved to vdb successfully!###")
        print()
    except Exception as e:
        print("!!!Faled to save recent chat vdb!!!")
        print(e)
        print()


def delete_vdb():
    # clean vdb data
    try:
        vdb.vdb.delete_collection()
        vdb.vdb.persist()
        # Force remove the folder
        shutil.rmtree("database/vdb/")

        print("###Successfully delete vdb!###")
    except ValueError as e:
        print("!!!vdb collection does not exits!!!")
    except Exception as e:
        print(e)
    

    # Reset vdb
    try:
        # After remove long-term memory, create another new one with primed knowledge
        vdb.vdb = Chroma.from_texts(INFORMATION_ABOUT_JAY, persist_directory=VDB_DIR, embedding=OpenAIEmbeddings())
        vdb.retriever = vdb.vdb.as_retriever(search_kwargs=dict(k=5))
        vdb.v_memory = VectorStoreRetrieverMemory(retriever=vdb.retriever)
    except Exception as e:
        print(f"!!!Failed to create a new vdb!!!")
        print(e)


vdb = VDB()

if __name__ == '__main__':
    pass