from flask import Flask, request, jsonify, abort, flash
from sqlalchemy import Column, String, Integer
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db.init_app(app)


class MovieDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    year = db.Column(db.String)


with app.app_context():
    db.create_all()
    print('Database connected')


# @app.route('/get_movie', methods=['GET'])
# def get_movies():
#     return jsonify(movies)

@app.route('/add_movie', methods=['POST'])
def add_movie():
    title = request.args.get('title')
    response = requests.get(f'http://www.omdbapi.com/?t={title}&apikey=...')
    data = response.json()
    movies = MovieDB(
        title=data.get('Title'),
        year=data.get('Year', 'N/A')
    )

    db.session.add(movies)
    db.session.commit()
    return jsonify(
        {
            'title': movies.title,
            'year': movies.year
        }
    )


@app.route('/delete_movie/<int:id>', methods=['DELETE'])
def del_movie(id):
    movie_to_del = MovieDB.query.get_or_404(id)
    db.session.delete(movie_to_del)
    db.session.commit()
    return jsonify({"message": "Movie deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
