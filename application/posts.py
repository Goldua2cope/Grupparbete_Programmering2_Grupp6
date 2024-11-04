from flask import jsonify, request , session
import sqlite3

def home():
    with sqlite3.connect('blogs.db') as con: 
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        comments = cur.execute('''
            SELECT comments.Comment_ID, comments.Comment_Description ,
                   posts.Post_ID, posts.Post_title, posts.Post_Description
            FROM posts
            LEFT JOIN comments ON posts.Post_ID = comments.Post_ID
        ''').fetchall()
        
        comments_list = []
        
        for comment in comments:
            comment_dict = { 
                'Comment_ID': comment['Comment_ID'],        
                'Comment_Description': comment['Comment_Description'],
                'Post_ID': comment['Post_ID'],
                'Post_title': comment['Post_title'],
                'Post_Description': comment['Post_Description']
            }
            comments_list.append(comment_dict)
    
    return jsonify(comments_list), 200

def add_post():
    print("Session contents :", dict(session))
    if 'username' not in session:
        return jsonify({'Error': 'You have to be logged in to crate a post.'}), 400
     
    data = request.get_json(silent=True)
    if data is None:
        return  jsonify({'Error':'Null value.'})
    title = data.get('Post_title')
    description = data.get('Post_Description')
    
    if not title or not description :
        return jsonify({'Error': 'Post_title and Post_Description are required.'}), 400

    user_id = session['user_id']
    with sqlite3.connect('blogs.db') as con:
        cur = con.cursor()
        #### har lagt till User_ID för att veta vem har skrivit den och bara hen kan radera den
        cur.execute('''INSERT INTO posts ( Post_title, Post_Description, User_ID) 
                        VALUES (?,?,?)''', 
                        (title, description,user_id))
        con.commit()
        return jsonify({'Message': 'Your post has been created successfully.'}), 201


def delete_post():
    if 'username' not in session:
        return jsonify({'Error': 'You must be logged in to delete a post.'}) , 400

    data = request.get_json(silent=True)
    if data is None:
        return  jsonify({'Error':'Null value.'})
    post_id = data.get('Post_ID')

    if not post_id:
        return jsonify({'Error': 'Post_ID is required.'}), 400
    
    with sqlite3.connect('blogs.db') as con:
        cur = con.cursor()
        
        user_id = session['user_id']

        cur.execute('SELECT User_ID FROM posts WHERE Post_ID = ?', (post_id,))
        user_result = cur.fetchone()

        if user_result == None:
            return jsonify({'Error':'Post not found'}) , 404
        elif user_result[0] != user_id:
            return jsonify({'Error':'You do not have permission to delete this post.'})
        else:
            cur.execute('DELETE FROM posts WHERE Post_ID = ?', (post_id,))
            con.commit()
            return jsonify({'Message': 'Your post has been deleted.'}), 200
   
