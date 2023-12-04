from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/your_database'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)

# Create tables in the database
db.create_all()

# Endpoint 1: Retrieve All Books
@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        books = Book.query.all()
        book_list = [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]
        return jsonify(book_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint 2: Add a New Book
@app.route('/api/books', methods=['POST'])
def add_new_book():
    try:
        data = request.get_json()
        new_book = Book(title=data['title'], author=data['author'])
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'message': 'Book added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint 3: Update Book Details
@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book_details(id):
    try:
        book = Book.query.get(id)
        if book is None:
            return jsonify({'error': 'Book not found'}), 404

        data = request.get_json()
        book.title = data['title']
        book.author = data['author']
        db.session.commit()

        return jsonify({'message': 'Book updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
