import sqlite3

class Database:
    def __init__(self):
        self.db_name = "database.db"
        self.table_name = "fans_table"
        self.create_table()
    
    def create_table(self):
        query_make_table = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userName TEXT,
                userContact TEXT
                )   
            """
        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute(query_make_table)
        
        conn.commit()
        conn.close()
    
    def insert_value(self, name, phone):

        query_insert_value = f'''
                    INSERT INTO {self.table_name} (userName, userContact)
                    VALUES (?, ?)
                '''
        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute(query_insert_value, (name, phone))
        
        conn.commit()
        conn.close()

    def fetch_data(self):
        query_fetch_data = f'SELECT * FROM {self.table_name}'

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute(query_fetch_data)
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        return data
    
    def delete_data(self, id):
        query_del_entry = f'DELETE FROM {self.table_name} WHERE id = ?'
        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute(query_del_entry, (id,))
        
        conn.commit()
        conn.close()