from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Creates database with all information about user and posts
def init_db():
    con = sqlite3.connect('blogs.db')
    cursor = con.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                   User_ID INTEGER PRIMARY KEY, 
                   USERNAME TEXT NOT NULL,
                   PASSWORD TEXT NOT NULL
                   )                  
''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                   Post_ID AUTO_INCREMENT PRIMARY KEY,
                   User_ID INTEGER NOT NULL, 
                   Post_title TEXT NOT NULL,
                   Description TEXT,
                   Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY(User_ID) REFERENCES users(User_ID)
                   )                  
''')      
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                   Comment_ID AUTO_INCREMENT PRIMARY KEY,
                   User_ID INTEGER NOT NULL, 
                   Post_ID INTEGER NOT NULL,
                   Description TEXT NOT NULL,
                   Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY(Post_ID) REFERENCES posts(Post_ID)
                   FOREIGN KEY(User_ID) REFERENCES users(User_ID)
                   )                  
''')
    con.commit()
    con.close()

init_db()

@app.route('/', methods=['GET'])
def home():
    con = sqlite3.connect('blogs.db')
    cur = con.cursor()
    posts = cur.execute('''SELECT Post_title, User_ID, Description, Created_at FROM posts 
                        JOIN users ON posts.User_ID = users.User_ID''').fetchall()
    con.close()
    return jsonify(dict(posts)), 200

@app.route('/post', methods=['POST'])
def add_post():
    data = request.get_json()
    title = data.get('Post_title')
    description = data.get('Description')

    con = sqlite3.connect('blogs.db')
    cur = con.cursor()
    cur.execute('INSERT INTO posts (Post_title, Description) VALUES (?, ?)', (title, description))
    con.commit()
    con.close()

    return jsonify({'Message': 'Your post has been created successfully.'}), 201

@app.route('/post', methods=['DELETE'])
def delete_post(post_id):
    data = request.get_json()
    post_id = data.get('Post-ID')

    con = sqlite3.connect('blogs.db')
    cur = con.cursor()
    cur.execute('DELETE FROM posts WHERE Post-ID = (?)', (post_id))
    
    return jsonify({'Message': 'Your post has been delected.'}), 200

@app.route('/comment', methods=['POST'])
def add_post():
    data = request.get_json()
    title = data.get('Post_title')
    description = data.get('Description')

    con = sqlite3.connect('blogs.db')
    cur = con.cursor()
    cur.execute('INSERT INTO posts (Post_title, Description) VALUES (?, ?)', (title, description))
    con.commit()
    con.close()

    return jsonify({'Message': 'Your post has been created successfully.'}), 201

@app.route('/comment', methods=['DELETE'])
def delete_post():
    data = request.get_json()
    post_id = data.get('Post-ID')

    con = sqlite3.connect('blogs.db')
    cur = con.cursor()
    cur.execute('DELETE FROM posts WHERE Post-ID = (?)', (post_id))
    
    return jsonify({'Message': 'Your post has been delected.'}), 200
