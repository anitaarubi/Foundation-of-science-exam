 import useful external libraries
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# flask setup; specify database name; error debug; initialize database
app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///aaldb.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# create a class model for the database
class Book(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    publication_year = db.Column(db.Integer)

    def _init_(self, title, author, publication_year):
        self.title = title
        self.author = author
        self.publication_year = publication_year

# html index page
@app.route("/books")
def index():
    return render_template("books.html", db_table = Book.query.all())

# html add-user page
@app.route('/add_book', methods = ["POST", "GET"])
def add_user():
    if request.method == "POST":
        # collect input from user
        user_title = request.form["title"]
        user_author = request.form["author"]
        user_publication_year = request.form["publication_year"]

        # ignore entries if all user input is empty 
        if (user_title == user_author == user_publication_year == ""): 
            return render_template("add_book.html")

        # pass user input to database
        user_input = Book(user_title, user_author, user_publication_year)
        db.session.add(user_input)
        db.session.commit()

        return render_template("add_book.html")
    else:
        return render_template("add_book.html")

# run the program
if _name_ == "_main_":
    with app.app_context(): db.create_all()
    app.run(debug=True)