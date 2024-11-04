from flask import jsonify, request , session
import sqlite3


def add_comment():
    if 'username' not in session:
        return jsonify({'Error': 'You have to be logged in to create a comment.'}), 400
        
    data = request.get_json(silent=True)
    if data is None:
        return  jsonify({'Error':'Null value.'})
    post_id = data.get('Post_ID') 
    description = data.get('Comment_Description')
    
    if not post_id or not description:
        return jsonify({'Error': 'Post_ID och Comment_Description are required.'}), 400
    
    user_id = session['user_id']
    
    with sqlite3.connect('blogs.db') as con:
        cur = con.cursor()
        ###kontrollera om post finns
        cur.execute('SELECT * FROM posts WHERE Post_ID = ?', (post_id,))
        post_exists = cur.fetchone()
        
        if not post_exists:
            return jsonify({'Error': 'Post_ID does not exist.'}), 404
        
        cur.execute('''INSERT INTO comments (Post_ID, Comment_Description, User_ID) 
                        VALUES (?,?,?)''', 
                        (post_id, description,user_id))
        con.commit()
        return jsonify({'Message': 'Your comment has been added.'}), 201

def delete_comment():
    if 'username' not in session:
        return jsonify({'Error': 'You must be logged in to delete a comments.'})
    
    data = request.get_json(silent=True)
    if data is None:
        return  jsonify({'Error':'Null value.'})
    comment_id = data.get('Comment_ID')
    user_id = session['user_id']

    if not comment_id:
        return jsonify({'Error':'Comment_ID is required.'}) , 400
    
    with sqlite3.connect('blogs.db') as con:
        cur = con.cursor()
        cur.execute('SELECT User_ID FROM comments WHERE Comment_ID = ?', (comment_id,))
        user_result = cur.fetchone()
        
        if user_result == None:
            return jsonify({'Error':'Comment not found'}) , 404
        if user_result[0] != user_id :
            return jsonify({'Error':'You do not have permission to delete this post.'})
        else:
            cur.execute('DELETE FROM comments WHERE Comment_ID = ?', (comment_id,))
            con.commit()
            return jsonify({'Message': 'Your comment has been deleted.'}), 200
        
