from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

from sqlalchemy.testing.suite.test_reflection import users

from models import db
from models.user import User
from models.game import Game
from models.loans import Loan
from models.customer import Customer
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
@app.route('/loan', methods=['POST'])
def loan_game():
    try:
        data = request.json
        customer_id = data.get('customer_id')
        game_id = data.get('game_id')

        # Check if game is already loaned and not returned
        existing_loan = Loan.query.filter_by(game_id=game_id, return_date=None).first()
        if existing_loan:
            return jsonify({'error': 'This game is already loaned'}), 400

        # Create new loan
        new_loan = Loan(client_id=customer_id, game_id=game_id)
        db.session.add(new_loan)
        db.session.commit()

        return jsonify({'message': 'Game successfully loaned'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to loan game', 'message': str(e)}), 500

@app.route('/games', methods=['GET'])
def get_games():
    try:
        games = Game.query.all()

        games_list = []
        for game in games:
            is_loaned = Loan.query.filter_by(game_id=game.id, return_date=None).first() is not None
            games_list.append({
                'id': game.id,
                'name': game.name,
                'price': game.price,
                'quantity': game.quantity,
                'is_loaned': is_loaned
            })

        return jsonify({'message': 'Games retrieved successfully', 'games': games_list}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve games', 'message': str(e)}), 500

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

# Add Client
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    if not data.get('name') or not data.get('phone_number') or not data.get('email'):
        return jsonify({"error": "Name, phone number, and email are required"}), 400

    existing_customer = Customer.query.filter(
        (Customer.phone_number == data['phone_number']) | (Customer.email == data['email'])
    ).first()
    if existing_customer:
        return jsonify({"error": "Customer with this phone number or email already exists"}), 400

    new_customer = Customer(name=data['name'], phone_number=data['phone_number'], email=data['email'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(
        {"message": "Customer added successfully!", "Customer": {"id": new_customer.id, "name": new_customer.name}}), 201

# Get All Customers
@app.route('/customers', methods=['GET'])
def get_clients():
    customers = Customer.query.all()
    customers_list = [{"id": c.id, "name": c.name, "phone": c.phone_number, "email": c.email} for c in customers]
    return jsonify({"customers": customers_list})

# Delete Customer
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def drop_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully!"}), 200


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