from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from models import db
from models.user import User
from models.game import Game
from models.loans import Loan

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


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # Generate token
            token = jwt.encode(
                {
                    'user_id': user.id,
                    'username': user.username,
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
    with app.app_context():
        db.create_all()  # Create all database tables as per the models
        # db.drop_all()  # Create all database tables as per the models
        new_user = User(
            name = 'Oron',
            phone_number = '0501234567',
            age = 18
        )
        db.session.add(new_user)
        db.session.commit()
    app.run(debug=True)  # Start the Flask application in debug mode
