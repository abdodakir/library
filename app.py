"""  """
from flask import Flask
from flask import jsonify, request
from pymongo import MongoClient

client = MongoClient('localhost:27017')
app = Flask(__name__)

# database
db = client.library
#export FLASK_ENV=development

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return jsonify({'message': 'Welcome to Your Library'}), 201

@app.route('/books', methods=['GET', 'POST'])
def list_books():
    books = db.books
    if request.method == 'GET':
        data = request.get_json()
        # print("***************************")
        # print(data)
        # print("***************************")
        # return jsonify(data)
    else:
        data = request.get_json()
    book = {}

    if "action" in data:
        # create a new book
        if data['action'] == 'create':
            if "isbn" in data:
                org = books.find_one({'isbn': data.get("isbn")})
                if org :
                    return jsonify({"success": False, "message": "this book exist"}), 301
                book["isbn"] = data.get("isbn")
                book['titre_book'] = data.get("titre")
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
            pass
        # get a list of books
        if data["action"] == "get_books":
            orgs = [item for item in books.find()]
            return jsonify({"success": True, "books": orgs}), 201
        else:
            return jsonify({"success": False, "action": "action error"}), 301    
    else:
        return jsonify({"success": False, "action": "not exist"}), 301

@pp.route('/users', methods['GET', 'POST'])
def users():
    pass



if __name__ == '__main__':
    app.run()