from flask import jsonify
import sqlite3

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
        
        result = []
        for entry in posts_and_comments:
            result[entry['Post_title']] = {
                'Post_ID': entry['Post_ID'],
                'Post_title': entry['Post_title'],
                'Creator': entry['Username'],
                'Created': entry['Post_created_at'],
                'Comments': []
            }
            
            if entry['Comment_ID'] is not None:
                result[entry['Post_title']]['Comments'].append({
                    'Comment_ID': entry['Comment_ID'],
                    'Created': entry['Comment_created_at'],
                    'Comment_description': entry['Comment_description']
                })

    return jsonify(result), 200

# TODO: SKRIVT UT ALLA KOMMENTARER

def get_post(post_id):
    with sqlite3.connect('blogg_data.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        post = cur.execute('''SELECT posts.Post_ID, posts.Post_title, posts.Post_description, posts.Post_created_at,
                    users.Username
                    From posts
                    Join users ON posts.User_ID = users.User_ID
                    WHERE posts.Post_ID = ?
                    ''', (post_id,))
        result = []

        return cur.fetchone()

def add_post(user_id, title, post_description):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('''INSERT INTO posts (User_ID, Post_title, Post_description) 
                        VALUES (?, ?, ?)''', 
                        (user_id, title, post_description))
        con.commit()
        
def update_post(user_id, post_id, post_description):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE posts 
                    SET Post_description = ? 
                    WHERE Post_ID = ? AND User_ID = ?
                    ''', (post_description, post_id, user_id))
        con.commit()
        if cur.rowcount == 0:
            return False
    return True

def delete_post(user_id, post_id):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('''DELETE FROM posts
                    WHERE Post_ID = ? AND User_ID = ?''', 
                    (post_id, user_id))
        con.commit()
        if cur.rowcount == 0:
            return False
    return True

def get_post_id(post_title):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('SELECT Post_ID FROM posts WHERE Post_title = ?',
                    (post_title,))
        return cur.fetchone()[0]