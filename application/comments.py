import sqlite3
from user import get_user_id

def add_comment(post_id: int, comment_description: str, user_id: int) -> int:
    """
    Lägger till en ny kommentar till ett specifikt inlägg i databasen 
    Ansluter till databasen, infogar en ny rad i 'comments'-tabellen med:
    Post-ID för inlägget som kommentaren tillhör, Användar-ID för den som skapar kommentaren och kommentartext. 
    Sparar ändringen och returnerar ID för den skapade kommentaren. 
    """

    with sqlite3.connect('blogg_data.db') as con:  
        cur = con.cursor()
        cur.execute('''INSERT INTO comments (Post_ID, User_ID, Comment_description) 
                    VALUES (?, ?, ?)''', 
                    (post_id, user_id, comment_description))
        con.commit()
        return cur.lastrowid    # Returnerar ID för den skapade kommentaren

def delete_comment(user_id: int, comment_id: int) -> bool:
    """
    Raderar en kommentar 
    Använder ett SQL-kommando som säkerställer att en kommentar raderas endast av den inloggade användaren som skapat kommentaren, 
    genom matchning av kommentarens- och användarens ID
    Returnerar True om raderingen lyckades, annars False 
    """

    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('DELETE FROM comments WHERE Comment_ID = ? AND User_ID = ?', 
                    (comment_id, user_id))
        con.commit()
        if cur.rowcount == 0:
            return False
    return True # Returnerar True om raderingen lyckas
