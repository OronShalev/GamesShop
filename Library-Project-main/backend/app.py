from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

from sqlalchemy.testing.suite.test_reflection import users

from models import db
from models.user import User
from models.game import Game
from models.loans import Loan
import jwt

app = Flask(__name__)  # create a flask instance
# Enable all routes, allow requests from anywhere (optional, not recommended for security)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database URI for SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)  # Initialize the database with the Flask application

# Route to add a new game (similar to adding a book)
@app.route('/games', methods=['POST'])
def add_game():
    try:
        data = request.json
        new_game = Game(
            name=data['name'],
            price=data['price'],
            quantity=data['quantity']
        )
        db.session.add(new_game)
        db.session.commit()
        return jsonify({'message': 'Game added to the database.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add game', 'message': str(e)}), 500


# Route to retrieve all games
@app.route('/games', methods=['GET'])
def get_games():
    try:
        games = Game.query.all()  # Retrieve all games from the database

        # Create an empty list to store formatted game data
        games_list = []

        for game in games:  # Loop through each game
            game_data = {
                'id': game.id,
                'name': game.name,
                'price': game.price,
                'quantity': game.quantity
            }
            # Add the game dictionary to the list
            games_list.append(game_data)

        return jsonify({
            'message': 'Games retrieved successfully',
            'games': games_list
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve games',
            'message': str(e)
        }), 500

@app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    try:
        game = Game.query.get(game_id)
        if not game:
            return jsonify({'error': 'Game not found'}), 404

        db.session.delete(game)
        db.session.commit()
        return jsonify({'message': 'Game deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete game', 'message': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        phone_num = data.get('phone_num')
        password = data.get('password')

        user1 = User.query.filter_by(phone_number=phone_num).first()

        if user1 and user1.check_password(password):
            token = jwt.encode(
                {
                    'user_id': user1.id,  # Corrected reference to user1
                    'exp': datetime.utcnow() + timedelta(hours=24)
                },
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            return jsonify({'token': token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500

if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'your_secret_key'  # Ensure a secret key is set

    with app.app_context():
        db.create_all()

        # Check if test user exists
        test_user = User.query.filter_by(phone_number='0501234567').first()
        if not test_user:
            print("Creating test user...")
            new_user = User(
                name='Oron',
                phone_number='0501234567',
                age=18
            )
            new_user.set_password("pass")  # Hash the password
            db.session.add(new_user)
            db.session.commit()

        # Print all users for verification
        users = User.query.all()
        print("\nCurrent users in database:")
        for user in users:
            print(f"ID: {user.id}, Name: {user.name}, Phone: {user.phone_number}")

    app.run(debug=True)