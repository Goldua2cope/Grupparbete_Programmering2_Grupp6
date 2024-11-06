import sqlite3

def register(username: str, password: str) -> None:
    """
    Registrerar en ny användare i databasen.
    """
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        cur.execute('''INSERT INTO users (Username, Password) VALUES (? , ?)''', 
                    (username, password))
        con.commit()
   
def check_credentials(username: str, password: str) -> tuple | None :
    """
    Kontrollerar användarens inloggningsuppgifter.
    Returnerar en tuple med användarnamn och lösenord om de matchar, annars None.
    """
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        return cur.execute('''SELECT Username, Password FROM users 
                Where Username = ? AND Password = ?''', 
                (username, password)).fetchone()

def check_status(user_id: int) -> int:
    """
    Kontrollerar användarens status.
    Returnerar användarens statusvärde.
    """
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        user_status = cur.execute('SELECT Status FROM users WHERE User_ID = ?', 
                           (user_id,)).fetchone()
        return user_status[0]

def get_user_id(username: str) -> int:
    """
    Hämtar användar-ID baserat på användarnamn.
    Returnerar användarens ID.
    """
    with sqlite3.connect('blogg_data.db') as con:
        cur = con.cursor()
        user_id = cur.execute('SELECT User_ID from users WHERE Username = ?', 
                           (username,)).fetchone()
        return user_id[0]

def change_status(user_id: int, value: int) -> None:
    """ Ändrar användarens status i databasen."""
    
    with sqlite3.connect('blogg_data.db') as con: 
        cur = con.cursor()
        cur.execute('UPDATE users SET Status = ? WHERE User_ID = ?',
                    (value, user_id))
        con.commit()

def check_login(session: dict) -> bool:
    """
    Kontrollerar om användaren är inloggad.
    Returnerar True om användaren är inloggad, annars False.
    """
    
    if 'username' in session and check_status(session.get("user_id", 0)) == 1:
        return True
    return False
