import sqlite3

def posts_and_comments()-> list[dict]:
    """ 
    Hämtar alla inlägg med tillhörande kommentarer från databasen.
    Returnerar en lista av inlägg där varje inlägg är en dictionary
    som innehåller inläggets information och en lista av dess kommentarer..
    """

    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        result = []
        
        posts = cur.execute('''SELECT Post_ID, Post_title, Post_description, Post_created_at, User_ID FROM posts''').fetchall()
        for post in posts:
            current_post = {
                'Post_ID': post[0],
                'User_ID': post[4],
                'Post_title': post[1],
                'Post_description': post[2],
                'Post_created_at': post[3],
                'comments': []
            }
            comments = cur.execute('''SELECT Comment_ID, Comment_description, Comment_created_at, User_ID FROM comments WHERE Post_ID = ?''', 
                                   (post[0],)).fetchall()
            for comment in comments:
                current_post['comments'].append({
                    'comment_ID': comment[0],
                    'comment_description': comment[1],
                    'comment_created_at': comment[2],
                    'User_ID': comment[3]
                })
            result.append(current_post)

    return result

def get_post(post_id: int) -> dict | None:
    """
    Hämtar ett specifikt inlägg med dess kommentarer baserat på inläggets ID.
    Returnerar en dictionary med inläggets information och tillhörande kommentarer,
    eller None om inlägget inte hittas
    """
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        post = cur.execute('SELECT * FROM posts WHERE Post_ID = ?', (post_id,)).fetchone()
        
        if post is None:
            return None
        
        found_post = {
            'Post_ID': post[0],
            'Post_title': post[2],
            'Post_description': post[3],
            'Post_created_at': post[4],
            'comments': []
        }
        comments = cur.execute('SELECT * FROM comments WHERE Post_ID = ?', (post_id,)).fetchall()
        for comment in comments:
            found_post['comments'].append({
                'comment_ID': comment[0],
                'comment_description': comment[3],
                'comment_created_at': comment[4]
            })
    return found_post

def add_post(user_id: int, title: str, post_description: str) -> int:
    """
    Lägger till ett nytt inlägg i databasen.
    Returnerar ID för det nyligen skapade inlägget.
    """

    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('''INSERT INTO posts (User_ID, Post_title, Post_description) 
                        VALUES (?, ?, ?)''', 
                        (user_id, title, post_description))
        con.commit()
    return cur.lastrowid
        
def update_post(user_id: int, post_id: int, post_description: str) -> bool:
    """
    Uppdaterar beskrivningen av ett specifikt inlägg.
    Returnerar True om uppdateringen lyckades, annars False.
    """
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

def delete_post(user_id: int, post_id: int) -> bool:
    """
    Raderar ett specifikt inlägg och alla dess tillhörande kommentarer.
    Returnerar True om raderingen lyckades, annars False.
    """
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        deleted_posts = cur.execute('''DELETE FROM posts
                    WHERE Post_ID = ? AND User_ID = ?''', 
                    (post_id, user_id)).rowcount
        cur.execute('''DELETE FROM comments WHERE Post_ID = ?''', (post_id,))
        con.commit()
        if deleted_posts == 0:
            return False
    return True
