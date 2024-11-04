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
                   Post_description TEXT,
                   Post_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY(User_ID) REFERENCES users(User_ID)
                   )                  
''')      
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                   Comment_ID INTEGER PRIMARY KEY,
                   User_ID INTEGER NOT NULL, 
                   Post_ID INTEGER NOT NULL,
                   Comment_description TEXT NOT NULL,
                   Comment_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY(Post_ID) REFERENCES posts(Post_ID),
                   FOREIGN KEY(User_ID) REFERENCES users(User_ID)
                   )                  
''')
    con.commit()
    con.close()

def posts_and_comments():
    with sqlite3.connect('blogg_data.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        posts_and_comments = cur.execute('''SELECT users.Username,
                                         posts.Post_ID, posts.Post_title, posts.Post_description, posts.Post_created_at, 
                                         comments.Comment_ID, comments.Comment_description, comments.Comment_created_at
                                         FROM posts
                                         LEFT JOIN comments on posts.Post_ID = comments.Post_ID
                                         LEFT JOIN users on posts.User_ID = users.User_ID
                                         ORDER BY posts.Post_created_at
                                        ''').fetchall()
        
        for post in posts_and_comments:
            print(dict(post))

def get_post(post_id):
    with sqlite3.connect('blogg_data.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        post = cur.execute('''SELECT posts.Post_ID, posts.Post_title, posts.Post_description, posts.Post_created_at,
                    users.Username
                    From posts
                    Join users ON posts.User_ID = users.User_ID
                    WHERE posts.Post_ID = ?
                    ''', (post_id,)).fetchone()

        print(dict(post))

get_post(2)