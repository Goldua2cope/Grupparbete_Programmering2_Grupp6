from flask import jsonify, request
import sqlite3

# TODO: SKRIVA UT ALLA KOMMENTARER OCKSÅ

def home():
    con = sqlite3.connect('blogs.db')
    cur = con.cursor()
    posts = cur.execute('''SELECT Post_title, User_ID, Description, Created_at FROM posts 
                        JOIN users ON posts.User_ID = users.User_ID''').fetchall()
    con.close()
    return jsonify(posts), 200

def add_post():
    data = request.get_json()
    username = data.get('Username')
    title = data.get('Post_title')
    description = data.get('Description')
    
    with sqlite3.connect('blogs.db') as con:
        cur = con.cursor()

        cur.execute('''SELECT Logged_in FROM users 
                    Where Username = ?''', (username,))
    
    # If match is a tuple (1,0) which means logged in
        if cur.fetchone() == (1,):
            cur.execute('''INSERT INTO posts (Post_title, Description) 
                        VALUES (?, ?)''', 
                        (title, description))
            con.commit()
            return jsonify({'Message': 'Your post has been created successfully.'}), 201
        else: 
            return jsonify({'Error': 'You have to be logged in to crate a post.'}), 403

# TODO: LÄGG TILL CONDITIONS ATT ANVÄNDAREN BARA FÅ TA BORT SINA POSTS

def delete_post():
    data = request.get_json()
    username = data.get('Username')
    post_id = data.get('Post-ID')

    with sqlite3.connect('blogs.db') as con:
        cur = con.cursor()
    
        cur.execute('''SELECT Logged_in FROM users 
                 Where Username = ?''', (username,))
    
        if cur.fetchone() == (1,):
            cur.execute('DELETE FROM posts WHERE Post-ID = (?)', (post_id))
            con.commit()
            return jsonify({'Message': 'Your post has been delected.'}), 200
        else:
            return jsonify({'Error': 'You must be logged in to delete a post.'}) , 403

