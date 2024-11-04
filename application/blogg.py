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
    return posts.posts_and_comments()

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
        return jsonify({'Error': 'Invalid request.'}), 400

    post_title = data.get('Post_title')
    post_description = data.get('Description')
    post_id = data.get('Post_ID')
    
    if request.method == 'POST':
        if user.check_login(session) == False:
            return jsonify({'Error': 'You have to be logged in to create a post.'}), 401
        try:
            posts.add_post(session['user_id'], post_title, post_description)
            return jsonify({'Message': 'Your post has been successfully created.', 
                            'Post_ID:': f'{posts.get_post_id(post_title)}'}), 201
        except sqlite3.IntegrityError as e:
            return jsonify({'Error': f'{e}'}), 400
        
    if request.method == 'GET':
        post = posts.get_post(post_id)
        if post is None:
            return jsonify({'Error': 'Post not found'}), 404         
        return jsonify(post), 200

    if request.method == 'PUT':
        if user.check_login(session) == False:
            return jsonify({'Error': 'Unauthorized.'}), 401
       
        if not posts.update_post(session['user_id'], post_id, post_description):
            return jsonify({'Error': 'Post not found.'}), 404
        return jsonify({'Message': f'Post {post_id} has been updated.'}), 201
    
    if request.method == 'DELETE':
        if user.check_login(session) == False:
            return jsonify({'Error': 'Unauthorized.'}), 401
        
        if not posts.delete_post(session['user_id'], post_id):
            return jsonify({'Error': 'Post not found.'}), 404    
        return jsonify({'Message': f'Post {post_id} has been successfully deleted.'}), 200

@app.route('/comment', methods=['POST'])
def add_comment():
    return comments.add_comment()

@app.route('/comment', methods=['DELETE'])
def delete_comment():
    return comments.delete_comment()

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)
