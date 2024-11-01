from flask import jsonify, request , session
from app import app
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
    if 'username' not in session:
        return jsonify({'Error': 'You have to be logged in to crate a post.'}), 400
     
    data = request.get_json()
    title = data.get('Post_title')
    description = data.get('Description')
    
    with sqlite3.connect('blogs.db') as con:
        cur = con.cursor()


        cur.execute('''INSERT INTO posts (Post_title, Description) 
                        VALUES (?, ?)''', 
                        (title, description))
        con.commit()
        return jsonify({'Message': 'Your post has been created successfully.'}), 201

# TODO: LÄGG TILL CONDITIONS ATT ANVÄNDAREN BARA FÅ TA BORT SINA POSTS

def delete_post():
    if 'username' not in session:
        return jsonify({'Error': 'You must be logged in to delete a post.'}) , 400

    data = request.get_json()
    post_id = data.get('Post_ID')

    with sqlite3.connect('blogs.db') as con:
        cur = con.cursor()

        cur.execute('SELECT Post_ID FROM posts WHERE Username = ?', (session['username'],))
        user_result = cur.fetchone()

        if user_result == None:
            return jsonify({'Error':'Post not found'}) , 404
        else:
            cur.execute('DELETE FROM posts WHERE Post_ID = ?', (post_id))
            con.commit()
            return jsonify({'Message': 'Your post has been delected.'}), 200
   
