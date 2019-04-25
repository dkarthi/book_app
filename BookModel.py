from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import json
from settings import app


db = SQLAlchemy(app)

class Book(db.Model):
	__tablename__ = 'books'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(80),nullable=False)
	author = db.Column(db.String(80))
	isbn = db.Column(db.Integer)
	price = db.Column(db.Float)

	def json(self):
		return {'name' : self.name, 'price' : self.price, 'author' : self.author, 'isbn' : self.isbn}

	def add_book(_name, _price, _author, _isbn):
		new_book = Book(name=_name,author=_author,price=_price,isbn=_isbn)
		db.session.add(new_book)
		db.session.commit()

	def delete_book(_isbn):
		is_successful = Book.query.filter_by(isbn=_isbn).delete()
		db.session.commit()
		return bool(is_successful)

	def get_books():
		return [Book.json(book) for book in Book.query.all()]

	def get_book_byisbn(_isbn):
		book = Book.query.filter_by(isbn=_isbn).first()
		if book is not None:
			return Book.json(Book.query.filter_by(isbn=_isbn).first())
		return None

	def __repr__(self):
		book_object = {
		"name" : self.name,
		"author" : self.author,
		"price" : self.price,
		"isbn" : self.isbn
		}

		return json.dumps(book_object)







