from utils.config import CHAT_HISTRY_SQL
import sqlite3 
import atexit



# SQLite3
class ChatDB:
    def __init__(self):
        self.conn = sqlite3.connect(CHAT_HISTRY_SQL)
        self.cur = self.conn.cursor()
        self.create_table()
        # Make sure the db close when program exits
        atexit.register(self.close_db)
    
    def create_table(self):
        try:
            query = f"""CREATE TABLE IF NOT EXISTS chat_history
            (sender TEXT,
            text TEXT,
            time TEXT
            )"""
            self.cur.execute(query)
            self.conn.commit()
            print("###Successfull create chat history table###\n")
        except Exception as e:
            print("!!!Failed to create the chat history table!!!\n")
            print(e)
        
    def insert_data(self, chat_data: tuple):
        placeholders = ', '.join(['?' for _ in chat_data])
        query = f"""INSERT INTO chat_history (sender, text, time) VALUES ({placeholders})"""
        try:
            self.cur.execute(query, chat_data)
            self.conn.commit()    
            print("###Successfully insert chat dialigues into chat history table###\n")
        except Exception as e:
            print("!!!Failed to insert chat dialigues into the chat history table!!!\n")
            print(e)
        
    
    def select_whole_chat_history(self):
        query = f"""SELECT * FROM chat_history"""
        try:
            self.cur.execute(query)
            chat_history = self.cur.fetchall()
            print("###Successfully retrieve chat history from chat history table###\n")

        except Exception as e:
            print("!!!Failed to retrieve chat history from chat history table!!!\n")
            print(e)
        
        return chat_history
        
        
    def delete_table(self):
        try:
            query = f"DROP TABLE IF EXISTS chat_history"
            self.cur.execute(query)
            self.conn.commit()
            print("###Successfully delete chat history table###\n")
        except Exception as e:
            print("!!!Failed to delete chat history table!!!\n")
            print(e)
        
        # Create table again
        self.create_table()
        
        
    def close_db(self):
        if self.conn:
            self.cur.close()
            self.conn.close()


# Initialize chat db
chat_db = ChatDB()

def get_frontend_chat_history_from_sql():
    
    try:
        records = chat_db.select_whole_chat_history()
        print("###Succesfully retrieve whole chat history###\n")
    except Exception as e:
        print("!!!Failed to retrieve chat history from SQLite!!!\n")
        print(e)
        return None
        
    if records:
        chat_history = []
        for record in records:
            (sender, text, timestamp) = record
            # Modify time from %Y-%m-%d %H:%M:%S -> %H:%M
            h_m_s = timestamp.split()[-1]
            h_m = ":".join(h_m_s.split(":")[:-1])
            message = {"sender": sender, "text": text, "time": h_m}
            chat_history.append(message)
        return chat_history
        
    return []


def save_chat_dialogue_to_sql(message):
    chat_db.insert_data(message)

def delete_whole_chat_history_from_sql():
    chat_db.delete_table()

