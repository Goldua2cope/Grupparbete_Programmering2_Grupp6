from flask import jsonify
import sqlite3


# TODO: SKRIVA UT TRE KOMMENTARER OCKSÅ

def posts_and_comments():
    with sqlite3.connect('blogg_data.db') as con:
        con.cursor()
        posts = con.execute('''SELECT posts.Post_ID, posts.Post_title, posts.Description, posts.Created_at, 
                            users.Username
                            FROM posts 
                            JOIN users ON posts.User_ID = users.User_ID''').fetchall()
    return jsonify(posts), 200

# TODO: SKRIVT UT ALLA KOMMENTARER
def get_post(post_id):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('''SELECT posts.Post_ID, posts.Post_title, posts.Description, posts.Created_at,
                    users.Username
                    From posts
                    Join users ON posts.User_ID = users.User_ID
                    WHERE posts.Post_ID = ?
                    ''', (post_id,))
        return cur.fetchone()

def add_post(user_id, title, description):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('''INSERT INTO posts (User_ID, Post_title, Description) 
                        VALUES (?, ?, ?)''', 
                        (user_id, title, description))
        con.commit()

def update_post(user_id, post_id, description):
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('''UPDATE posts 
                    SET Description = ? 
                    WHERE Post_ID = ? AND User_ID = ?
                    ''', (description, post_id, user_id))
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