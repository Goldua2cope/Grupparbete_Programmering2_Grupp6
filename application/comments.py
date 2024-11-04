from flask import jsonify
import sqlite3

def add_comment(post_id, comment_description):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('''INSERT INTO comments (Post_ID, Comment_description) 
                    VALUES (?, ?)''', 
                    (post_id, comment_description))
        con.commit()

def delete_comment(user_id, comment_id):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('DELETE FROM comments WHERE Comment_ID = ? AND User_ID = ?', 
                    (comment_id, user_id))
        con.commit()
        if cur.rowcount == 0:
            return False
    return True

def get_comment_id(comment_description):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('SELECT Comment_ID FROM comments WHERE Comment_description = ?', 
                    (comment_description,))
        return cur.fetchone[0]

