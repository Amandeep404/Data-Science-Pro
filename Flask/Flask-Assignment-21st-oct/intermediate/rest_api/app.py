from flask import Flask, request
from flask_restful import Api,Resource

app = Flask(__name__)
api = Api(app)

def find_book(id):
    for book in data:
        if book['id'] == id:
            return book
    return None

data = [
    {'id':1, 'author':'John', 'book':'Python', 'price':100},
    {'id':2, 'author':'Smith', 'book':'Java', 'price':200},
    {'id':3, 'author':'Peter', 'book':'C++', 'price':300},
    {'id':4, 'author':'Bob', 'book':'C', 'price':400},
    {'id':5, 'author':'Tom', 'book':'C#', 'price':500},
    {'id':6, 'author':'Jerry', 'book':'PHP', 'price':600},
    {'id':7, 'author':'Mike', 'book':'Ruby', 'price':700},
    {'id':8, 'author':'Mary', 'book':'Perl', 'price':400},
    {'id':9, 'author':'David', 'book':'JavaScript', 'price':700},
    {'id':10, 'author':'Jack', 'book':'Swift', 'price':500}
]


class BoookResource(Resource):
    def get(self):
        return data
    def post(self):
        new_book = {
            'id':len(data)+1,
            'author':'New Author',
            'book':'New Book',
        }
        data.append(new_book)
        return new_book,201
    
class find_books_by_id(Resource):
    def get(self, book_id):
        book = find_book(book_id) 
        if book:
            return book
        return {'message':'Author not found'},404
    
    def put(self, book_id):
        book = find_book(book_id)
        if book:
            book['author'] = request.json['author']
            book['book'] = request.json['book']
            book['price'] = request.json['price']
            return book
        return {'message':'Book not found'},404
    
    def delete(self, book_id):
        global data
        book = find_book(book_id)
        if book:
            data.remove(book)
            return {'message':'Book deleted Successfully'}
        return {'message':'Book not found'},404
    
api.add_resource(BoookResource,'/books')
api.add_resource(find_books_by_id,'/books/<int:book_id>')

if __name__ == '__main__':
    app.run(debug=True)