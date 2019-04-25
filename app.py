from flask import Flask,jsonify,request,Response
import json
from settings import *
from BookModel import *

import jwt, datetime


app.config['SECRET_KEY'] = 'meow'

@app.route('/login')
def get_token():
  exp_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
  token = jwt.encode({'exp':exp_date},app.config['SECRET_KEY'],algorithm='HS256')
  return token


#GET /books?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTU4NzEyMDd9.oEN-gKIhw8AV5kcV5atCum_EriCNB3sc5ZWVB34Gylw

"""
@app.route('/books')
def get_books():
    token = request.args.get('token')
    try:
      jwt.decode(token,app.config['SECRET_KEY'])
    except Exception as e:
      return jsonify({'error':'Invalid Token'})
    return jsonify({'books':Book.get_books()})
"""
@app.route('/books')
def get_books():
    return jsonify({'books':Book.get_books()})
    #return Book.get_books()

#POST /books
#{
# 'name':'book_name',
# 'isbn':123,
# 'author':'author_name',
# 'price':9
#}

def isvalid_book(book): 
    if('name' in book):
        return True
    return False


@app.route('/books/<int:isbn>',methods=['DELETE'])
def delete_book(isbn):
  if (Book.delete_book(isbn)):
    response = Response("Deleted Successfully",status=204,mimetype='application/text')
    return response

  invalidBookErrorMsg = {
    "error" : "Book not found,unable to delete_book"
  }
  response = Response(json.dumps(invalidBookErrorMsg),status=404,mimetype='application/json')

  return response



@app.route('/books',methods=['POST'])
def add_books():
    book = request.get_json()
    #print (Book.get_book_byisbn(book['isbn']))
    if Book.get_book_byisbn(book['isbn']) is None:
            Book.add_book(book['name'],book['price'],book['author'],book['isbn'])
            response = Response("",201,mimetype='application/json')
            response.headers['Location'] = "/books/"+str(book['isbn'])
            return response
    else:
            response = Response("Book already exists",200,mimetype='application/json')
            return response
    
@app.route('/books/<int:isbn>')
def get_book_byisbn(isbn):
    req_book = Book.get_book_byisbn(isbn)
    return jsonify(req_book)

app.run(port=5000)



