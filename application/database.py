import sqlite3

def init_db():
    con = sqlite3.connect('blogg_data.db')
    cursor = con.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                   User_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                   Username TEXT NOT NULL UNIQUE,
                   Password TEXT NOT NULL,
                   Status INTEGER DEFAULT 0
                   )                  
''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                   Post_ID INTEGER PRIMARY KEY,
                   User_ID INTEGER NOT NULL, 
                   Post_title TEXT NOT NULL,
                   Description TEXT,
                   Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY(User_ID) REFERENCES users(User_ID)
                   )                  
''')      
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                   Comment_ID INTEGER PRIMARY KEY,
                   User_ID INTEGER NOT NULL, 
                   Post_ID INTEGER NOT NULL,
                   Description TEXT NOT NULL,
                   Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY(Post_ID) REFERENCES posts(Post_ID),
                   FOREIGN KEY(User_ID) REFERENCES users(User_ID)
                   )                  
''')
    con.commit()
    con.close()
