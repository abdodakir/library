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

@app.route('/books', methods=['GET'])
def list_books():
    """ get a list of books """
    books = db.books
    book = {}
    if request.method == 'GET':
        data = request.get_json()
        if "action" in data:
            if data["action"] == "get_books":
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
                orgs = [serial(item) for item in books.find({}, book)]
                return jsonify({"success": True, "books": orgs}), 201
            else:
                return jsonify({"success": False, "action": "action error"}), 400
        else:
            return jsonify({"success": False, "action": "not exist"}), 400
    else:
        return jsonify({"error": "request failed"}), 401

@app.route('/create_book', methods=['POST'])
def create_book():
    """ create, update or delete a book """
    books = db.books
    book = {}
    if request.method == 'POST':
        data = request.get_json()
        if "action" in data:
            # create a new book
            if data['action'] == 'create':
                if "isbn" in data and data['isbn'] !="":
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
            if data["action"] == "delete":
                if "isbn" in data:
                    try:
                        books.delete_one({"isbn": data.get("isbn")})
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
    """ get a list of users """
    users = db.users
    user = {}
    if request.method == 'GET':
        data = request.get_json()
        if "action" in data:
            if data["action"] == "get_users":
                orgs = [serial(item) for item in users.find({}, user)]
                return jsonify({"success": True, "users": orgs}), 201
            else:
                return jsonify({"success": False, "action": "action error"}), 400
        else:
            return jsonify({"success": False, "action": "not exist"}), 400
    else:
        return jsonify({"error": "request failed"}), 501

@app.route('/register', methods=['POST'])
def register():
    """  """
    users.db.users
    user = {}
    if request.method == 'POST':
        data = request.get_json()
        if 'action' in data:
            if data['action'] == 'create':
                if data.get("password") != "":
                    pw_hash = bcrypt.generate_password_hash(data.get("password"))
                else:
                    pw_hash=""
                user['username'] = data.get("username", "")
                user['password'] = pw_hash
                user['type_user'] = data.get("type_user", "")
                user['last_name'] = data.get("last_name", "")
                user['first_name'] = data.get("first_name", "")
                user['date_born'] = data.get("date_born", "")
                user['scolar_year'] = data.get("scolar_year", "")
                user['classe'] = data.get("classe", "")
                user['nbr_emprunt'] = data.get("nbr_emprunt", 0)
                user['mail'] = data.get("mail", "")
                user['phone'] = data.get("phone", "")
                user['book_yet'] = data.get("book_yet", [])
                user['book_read'] = data.get("book_read", [])
                user['address'] = data.get("address", {})
                try:
                    user_id = users.insert_one(user)
                    print(user_id.inserted_id) 
                except expression as e:
                    return jsonify({"success": False, "error": e}), 400
                return jsonify({"success": True}), 201
        else:
            return jsonify({"success": False, "action": "action error"}), 400
    else:
        return jsonify({"error": "request failed"}), 501

@app.route('/login', methods=['GET'])
def login():
    """  """
    users = db.users
    user = {}
    if request.method == 'GET':
        data = request.get_json()
        if "action" in data:
            if data["action"] == 'login' and data['username'] != "":
                ur = users.find_one({'username': data.get("username")})
                if ur is not None:
                    if bcrypt.check_password_hash(ur['password'], data.get('password')):
                        return jsonify({'success': True, 'user': serial(ur)})
                    else:
                        return jsonify({'success': False, 'message': 'wrong password'})
                else:
                    return jsonify({'success': False, 'message': 'username doesn\'t exist'}), 400
            else:
                return jsonify({"success": False, "action": "action error"}), 400
        else:
            return jsonify({"success": False, "action": "not exist"}), 400
    else:
        return jsonify({"error": "request failed"}), 501



if __name__ == '__main__':
    app.run()