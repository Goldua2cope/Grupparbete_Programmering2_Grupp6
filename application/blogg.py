from flask import Flask, jsonify, request ,session 
import sqlite3
import user
import posts
import comments
import database

app = Flask(__name__)
app.secret_key = 'VerySTRONGPassword'

@app.route('/session_data')
def session_data():
    print(session)
    return jsonify(dict(session))

@app.route('/', methods=['GET'])
def home():
    return posts.posts_and_comments(), 200

@app.route('/register', methods=['POST'])
def register():
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

@app.route('/login', methods=['POST'])
def login():
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

@app.route('/logout', methods=['POST'])
def logout():
    if user.check_login(session):
        user.change_status(session['user_id'], 0)
        session.clear()
        return jsonify({'Message': 'You are now logged out.'}), 200
    else: 
        return jsonify({'Error': 'You are not logged in.'}), 401

@app.route('/post', methods=['POST', 'GET', 'PUT', 'DELETE'])
def post():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'Error': 'Bad request.'}), 400

    post_title = data.get('Post_title')
    post_description = data.get('Description')
    post_id = data.get('Post_ID')
    
    if request.method == 'POST':
        if not user.check_login(session):
            return jsonify({'Error': 'You have to be logged in for this function.'}), 401
        try:
            posts.add_post(session['user_id'], post_title, post_description)
            return jsonify({'Message': 'Your post has been successfully created.', 
                            'Post_ID:': f'{posts.get_post_id(post_title)}'}), 201
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

@app.route('/comment', methods=['POST', 'DELETE'])
def comment():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'Error': 'Bad request.'}), 400
    
    data = request.get_json()

    if request.method == ['POST']:
        post_id = data.get('Post_ID')
        comment_description = data.get('Comment_description')

        if not user.check_login(session):
            return jsonify({'Error': 'You have to be logged in for this function.'}), 401

        try:
            comments.add_comment(post_id, comment_description)
            return jsonify({'Message': 'Comment successfully added to post.', 
                            'Comment_ID': f'{comments.get_comment_id(comment_description)}'}), 201
        except sqlite3.IntegrityError as e:
            return jsonify({'Message': f'Bad request: {e}'}), 400

    if request.method == ['DELETE']:
        comment_id = data.get('Comment_ID')

        if not user.check_login(session):
            return jsonify({'Error': 'You have to be logged in for this function.'}), 401

        if not comments.delete_comment(session['user_id'], comment_id):
            return jsonify({'Error': 'Comment not found or unauthorized action for user.'}), 404 
        return jsonify({'Message': f'Comment {comment_id} has been deleted.'}), 200
    
if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)
