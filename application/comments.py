from flask import jsonify, request
import sqlite3

# TODO: ADD CONDITION FOR CHECKING IF POST EXISTS

def add_comment():
    data = request.get_json()
    username = data.get('Username')
    title = data.get('Post_title') # TODO: användbar för tidigare TODO
    description = data.get('Description')
    
    con = sqlite3.connect('blogs.db')
    cur = con.cursor()

    cur.execute('''SELECT Logged_in FROM users 
                Where Username = ?''', (username,))
    
    # If match is a tuple (1,0) which means logged in
    if cur.fetchone() == (1,):
        cur.execute('INSERT INTO comments (Description) VALUES (?, ?)', (description))
        con.commit()
        con.close()
        return jsonify({'Message': 'Your comment has been added.'}), 201
    else:
        con.close()
        return jsonify({'Error': 'You have to be logged in to create a comment.'}), 400


# TODO: LÄGG TILL CONDITIONS ATT ANVÄNDAREN BARA FÅ TA BORT SINA COMMENTS OCH OM DEN EXISTERAR

def delete_comment():
    data = request.get_json()
    username = data.get('Username')
    comment_id = data.get('Comment_ID')
    
    con = sqlite3.connect('blogs.db')
    cur = con.cursor()
    
    cur.execute('''SELECT Logged_in FROM users 
                Where Username = ?''', (username,))
    
    if cur.fetchone() == (1,):
        cur.execute('DELETE FROM posts WHERE Comment_ID = (?)', (comment_id))
        con.commit()
        con.close()
        return jsonify({'Message': 'Your comment has been delected.'}), 200
    else:
        con.close()
        return jsonify({'Error': 'You must be logged in to delete a comments.'})
