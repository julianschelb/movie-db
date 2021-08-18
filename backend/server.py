from flask import Flask, escape, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    name = request.args.get("name" , "World")
    return f'Hello, {escape(name)}!'
    

@app.route('/movies')
def getMovies():

    try:
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        # Fetch all record
        sql = """SELECT id, name, description, link FROM movies"""
        cursor.execute(sql)
        data = cursor.fetchall()

    except sqlite3.Error as error:
        response = jsonify("Failed to fetch records " + error)
        response.status_code = 500
        return response
    finally:
        if con: con.close()

    response = jsonify(data)
    response.status_code = 200
    #header = response.headers
    #header['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/movies/details')
def getMovieDetails():
    
    id = request.args.get("id", "")

    try:
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        # Fetch single record
        sql = """SELECT id, name, description, link FROM movies where id = ?"""
        cursor.execute(sql, (id,))
        data = cursor.fetchall()

        cursor.close()

    except sqlite3.Error as error:
        response = jsonify("Failed to fetch record " + error)
        response.status_code = 500
        return response
    finally:
        if con: con.close()

    response = jsonify(data)
    response.status_code = 200
    return response


@app.route('/movies/delete')
def deleteMovie():
    
    id = request.args.get("id", "")

    try:
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        # Deleting single record now
        sql = """DELETE from movies where id = ?"""
        cursor.execute(sql, (id,))
        con.commit()
        cursor.close()

    except sqlite3.Error as error:
        response = jsonify('Failed to delete record from sqlite table' + error)
        response.status_code = 500
        return response
    finally:
        if con: con.close()

    response = jsonify(f'Movie deleted with id {escape(id)}!')
    response.status_code = 200
    return response


@app.route('/movies/add', methods=['POST'])
def addMovie():

    movie = request.json
    name = movie['name']
    desc = movie['description']
    link = movie['link']

    con = sqlite3.connect('data.db')
    cursor = con.cursor()

    if name and desc and link and request.method == 'POST':			
        sql = "INSERT INTO movies (name, description, link) VALUES(?, ?, ?)"
        bindData = (name, desc, link,)
        cursor.execute(sql, bindData)
        con.commit()
        response = jsonify('Movie added successfully!')
        response.status_code = 200
        return response
    else:
        response = jsonify('Movie not added!')
        response.status_code = 500
        return response

@app.route('/movies/update', methods=['POST'])
def updateMovie():

    movie = request.json
    id = movie['id']
    name = movie['name']
    desc = movie['description']
    link = movie['link']

    con = sqlite3.connect('data.db')
    cursor = con.cursor()

    if id and name and desc and link and request.method == 'POST':			
        sql = "UPDATE movies SET name = ?, description = ?, link = ? WHERE id = ?"
        bindData = (name, desc, link, id, )
        cursor.execute(sql, bindData)
        con.commit()
        response = jsonify('Movie updated successfully!')
        response.status_code = 200
        return response
    else:
        response = jsonify('Movie not updated!')
        response.status_code = 500
        return response