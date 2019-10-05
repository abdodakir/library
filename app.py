"""  """
from flask import Flask
from flask import jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost:27017')
app = Flask(__name__)

# database
db = client.library
#export FLASK_ENV=development

def serial(dct):
    for k in dct:
        if isinstance(dct[k], ObjectId):
            dct[k] = str(dct['_id'])
    return dct

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return jsonify({'message': 'Welcome to Your Library'}), 201

@app.route('/books', methods=['GET', 'POST'])
def list_books():
    books = db.books
    book = {}
    if request.method == 'GET':
        data = request.get_json()
        # get a list of books
        if "action" in data:
            if data["action"] == "get_books":
                orgs = [serial(item) for item in books.find()]
                return jsonify({"success": True, "books": orgs}), 201
            else:
                return jsonify({"success": False, "action": "action error"}), 301
        else:
            return jsonify({"success": False, "action": "not exist"}), 301    
    
    if request.method == 'POST':
        data = request.get_json()
        if "action" in data:
            # create a new book
            if data['action'] == 'create':
                if "isbn" in data:
                    org = books.find_one({'isbn': data.get("isbn")})
                    if org :
                        return jsonify({"success": False, "message": "this book exist"}), 301
                    book["isbn"] = data.get("isbn")
                    book['title_book'] = data.get("title")
                    book["date_edition"] = data.get("date_edition")
                    book["specialite"] = data.get("specialite")
                    book["nbr_book"] = data.get("nbr_book")
                    book["auteur"] = data.get("auteur")
                    try:
                        book_id = books.insert_one(book)
                        print(book_id.inserted_id) 
                    except expression as e:
                        return jsonify({"success": False, "error": e})
                    return jsonify({"success": True})
            # Update book
            if data["action"] == "update":
                if "isbn" in data:
                    org = books.find_one({'isbn': data.get("isbn")})
                    if org :
                        book["isbn"] = data.get("isbn")
                        if data.get("title"):
                            book['title_book'] = data.get("title")
                        if data.get("date_edition"):
                            book["date_edition"] = data.get("date_edition")
                        if data.get("specialite"):    
                            book["specialite"] = data.get("specialite")
                        if data.get("nbr_book"):
                            book["nbr_book"] = data.get("nbr_book")
                        if data.get("auteur"):
                            book["auteur"] = data.get("auteur")
                        try:
                            isbn = data.get("isbn")
                            books.update_one( { 'isbn': isbn } ,{ "$set": book}) 
                        except expression as e:
                            return jsonify({"success": False, "error": e})
                    return jsonify({"success": True})
            else:
                return jsonify({"success": False, "action": "action error"}), 301
        else:
            return jsonify({"success": False, "action": "not exist"}), 301
    else:
        return jsonify({"error": "request failed"}), 401

@app.route('/users', methods=['GET', 'POST'])
def users():
    pass



if __name__ == '__main__':
    app.run()