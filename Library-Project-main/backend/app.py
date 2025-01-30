from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from models import db
from models.user import User
from models.book import Book
from models.loans import Loan


app = Flask(__name__)  # - create a flask instance
# - enable all routes, allow requests from anywhere (optional - not recommended for security)
CORS(app, resources={r"/*": {"origins": "*"}})


# Specifies the database connection URL. In this case, it's creating a SQLite database
# named 'library.db' in your project directory. The three slashes '///' indicate a
# relative path from the current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)  # initializes the databsewith the flask application


# this is a decorator from the flask module to define a route for for adding a book, supporting POST requests.(check the decorator summary i sent you and also the exercises)
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json  # this is parsing the JSON data from the request body
    new_book = Book(
        title=data['title'],  # Set the title of the new book.
        author=data['author'],  # Set the author of the new book.
        year_published=data['year_published'],
        # Set the types(fantasy, thriller, etc...) of the new book.
        types=data['types']
        # add other if needed...
    )
    db.session.add(new_book)  # add the bew book to the database session
    db.session.commit()  # commit the session to save in the database
    return jsonify({'message': 'Book added to database.'}), 201


# a decorator to Define a new route that handles GET requests
@app.route('/books', methods=['GET'])
def get_books():
    try:
        books = Book.query.all()                    # Get all the books from the database

        # Create empty list to store formatted book data we get from the database
        books_list = []

        for book in books:                         # Loop through each book from database
            book_data = {                          # Create a dictionary for each book
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'year_published': book.year_published,
                'types': book.types
            }
            # Add the iterated book dictionary to our list
            books_list.append(book_data)

        return jsonify({                           # Return JSON response
            'message': 'Books retrieved successfully',
            'books': books_list
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve books',
            'message': str(e)
        }), 500                                    #


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables defined in your  models(check the models folder)

    # with app.test_client() as test:
    #     response = test.post('/books', json={  # Make a POST request to /books endpoint with book  data
    #         'title': 'Harry Potter',
    #         'author': 'J.K. Rowling',
    #         'year_published': 1997,
    #         'types': '1'  # lets say 1 is fantasy
    #     })
    #     print("Testing /books endpoint:")
    #     # print the response from the server
    #     print(f"Response: {response.data}")

    #     #  GET test here
    #     get_response = test.get('/books')
    #     print("\nTesting GET /books endpoint:")
    #     print(f"Response: {get_response.data}")

    app.run(debug=True)  # start the flask application in debug mode

    # DONT FORGET TO ACTIVATE THE ENV FIRST:
    # /env/Scripts/activate - for windows
    # source ./env/bin/activate - - mac
