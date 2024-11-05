from flask import Flask, jsonify, request ,session 
import sqlite3
import user
import posts
import comments
import database

# Skapar Flask-applikationen
app = Flask(__name__)

# Sätter en hemlignyckel för sessionhantering
app.secret_key = 'VerySTRONGPassword'

# Hemrutt där alla inlägg och dess kommentarer visas
@app.route('/', methods=['GET'])
def home():
    """Hämtar alla inlägg och deras kommentarer."""
    
    return jsonify(posts.posts_and_comments()), 200

# Rutt för registrering av användare
@app.route('/register', methods=['POST'])
def register():
    """Registrerar en ny användare."""

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'Error': 'Invalid request.'}), 400
    
    username = data.get('Username')
    password = data.get('Password')

    try:
        user.register(username, password)
        return jsonify({'Message': 'User successfully created.'}), 201
    except sqlite3.IntegrityError as e:
        return jsonify({'Error': f'Bad request:{e}'}), 400

# Rutt för inloggning av användare
@app.route('/login', methods=['POST'])
def login():
    """Loggar in en användare."""

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'Error': 'Invalid request.'}), 400
    
    username = data.get('Username')
    password = data.get('Password')

    if user.check_credentials(username, password) is None:
        return jsonify({'Error': 'Wrong credentials.'}), 406
    if user.check_login(session):
        return jsonify({'Error' : 'You are already logged in.'}), 423
    
    session['username'] = username
    session['user_id'] = user.get_user_id(username)
    user.change_status(session['user_id'], 1)
    return jsonify({'Message': 'Welcome! You are now logged in.'}), 200

# Rutt för utloggning av användare 
@app.route('/logout', methods=['POST'])
def logout():
    """Loggar ut en användare."""

    if user.check_login(session):
        user.change_status(session['user_id'], 0)
        session.clear()
        return jsonify({'Message': 'You are now logged out.'}), 200
    else: 
        return jsonify({'Error': 'You are not logged in.'}), 401

# Rutt för hantering av inlägg 
@app.route('/post', methods=['POST', 'GET', 'PUT', 'DELETE'])
def post():
    """Hanterar CRUD-operationer för inlägg."""

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'Error': 'Bad request.'}), 400

    post_title = data.get('Post_title')
    post_description = data.get('Post_description')
    post_id = data.get('Post_ID')
    
    if request.method == 'POST':
        if not post_title or not post_description:
            return jsonify({'Error': 'Bad request: Missing title or description.'}), 400
        if not user.check_login(session):
            return jsonify({'Error': 'You have to be logged in for this function.'}), 401
        try:
            post_db_id = posts.add_post(session['user_id'], post_title, post_description)
            return jsonify({'Message': 'Your post has been successfully created.', 
                            'Post_ID:': f'{post_db_id}'}), 201
        except sqlite3.IntegrityError as e:
            return jsonify({'Error': f'Bad request: {e}'}), 400
        
    if request.method == 'GET':
        post = posts.get_post(post_id)
        if post is None:
            return jsonify({'Error': 'Post not found.'}), 404         
        return jsonify(post), 200 

    if request.method == 'PUT':
        if not user.check_login(session):
            return jsonify({'Error': 'Unauthorized: You must login first.'}), 401
       
        if not posts.update_post(session['user_id'], post_id, post_description):
            return jsonify({'Error': 'Post not found or unauthorized action for user.'}), 404
        return jsonify({'Message': f'Post {post_id} has been updated.'}), 201
    
    if request.method == 'DELETE':
        if not user.check_login(session):
            return jsonify({'Error': 'Unauthorized: You must log in first.'}), 401
        
        if not posts.delete_post(session['user_id'], post_id):
            return jsonify({'Error': 'Post not found or unauthorized action for user.'}), 404 
        return jsonify({'Message': f'Post {post_id} has been deleted.'}), 200

# Rutt för hantering kommentarer
@app.route('/comment', methods=['POST', 'DELETE'])
def comment():
    """Hanterar skapande och radering av kommentarer."""
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'Error': 'Bad request.'}), 400
    
    data = request.get_json()
    user_id = session.get('user_id')

    if request.method == 'POST':
        post_id = data.get('Post_ID')
        comment_description = data.get('Comment_description')
        
        if posts.get_post(post_id) is None:
            return jsonify({'Error': 'Post not found.'}), 404

        if not user.check_login(session):
            return jsonify({'Error': 'You have to be logged in for this function.'}), 401

        try:
            comment_id = comments.add_comment(post_id, comment_description, user_id)
            return jsonify({'Message': 'Comment successfully added to post.', 
                            'Comment_ID': f'{comment_id}'}), 201
        except sqlite3.IntegrityError as e:
            return jsonify({'Message': f'Bad request: {e}'}), 400

    if request.method == 'DELETE':
        comment_id = data.get('Comment_ID')

        if not user.check_login(session):
            return jsonify({'Error': 'You have to be logged in for this function.'}), 401

        if not comments.delete_comment(session['user_id'], comment_id):
            return jsonify({'Error': 'Comment not found or unauthorized action for user.'}), 404 
        return jsonify({'Message': f'Comment {comment_id} has been deleted.'}), 200
    
if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)

