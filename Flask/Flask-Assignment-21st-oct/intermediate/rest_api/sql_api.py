from flask import Flask, request
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    book = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"<Book {self.id}: {self.author} - {self.book}>"

with app.app_context(): 
    db.create_all()


class BookResource(Resource):
    def get(self):
        books = Book.query.all()
        return [{'id': book.id, 'author': book.author, 'book': book.book, 'price': book.price} for book in books]

    def post(self):
        new_book = Book(author='New Author', book='New Book', price=0.0)
        db.session.add(new_book)
        db.session.commit()
        return {'id': new_book.id, 'author': new_book.author, 'book': new_book.book, 'price': new_book.price}, 201


class FindBooksById(Resource):
    def get(self, book_id):
        book = Book.query.get(book_id)
        if book:
            return {'id': book.id, 'author': book.author, 'book': book.book, 'price': book.price}
        return {'message': 'Book not found'}, 404

    def put(self, book_id):
        book = Book.query.get(book_id)
        if book:
            book.author = request.json.get('author', book.author)
            book.book = request.json.get('book', book.book)
            book.price = request.json.get('price', book.price)
            db.session.commit()
            return {'id': book.id, 'author': book.author, 'book': book.book, 'price': book.price}
        return {'message': 'Book not found'}, 404

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'message': 'Book deleted successfully'}
        return {'message': 'Book not found'}, 404
    
    
api.add_resource(BookResource, '/books')
api.add_resource(FindBooksById, '/books/<int:book_id>')




if __name__ == '__main__':
    app.run(debug=True)