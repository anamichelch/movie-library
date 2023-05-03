from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my-movies-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(1000), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)


new_movie1 = Movie(
    title="Ana Michel",
    year=2012,
    description="Publicist  Shepard finds himself trapped in a phone booth, pinned down by an extortionist's"
                " sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads"
                " to a jaw-dropping climax.",
    rating=7.2,
    ranking=9,
    review="My favourite was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)

with app.app_context():
    db.create_all()
    # db.session.add(new_movie1)
    # db.session.commit()


@app.route("/")
def home():
    movies = Movie.query.all()
    return render_template("index.html", all_movies=movies)


@app.route("/edit")
def edit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template("edit.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
