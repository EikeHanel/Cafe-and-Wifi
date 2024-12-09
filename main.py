import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, func


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("APP_KEY")
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/cafes")
def cafes():
    all_cafes = db.session.execute(db.select(Cafe).order_by(func.lower(Cafe.name))).scalars().all()
    return render_template("cafes.html", all_cafes=all_cafes)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Get Cafe-Data from the Form
        cafe_name = request.form.get("name")
        cafe_map_url = request.form.get("map_url")
        cafe_img_url = request.form.get("img_url")
        cafe_location = request.form.get("location")
        cafe_seats = request.form.get("seats")
        cafe_has_toilet = True if request.form.get("has_toilet") == "on" else False
        cafe_has_wifi = True if request.form.get("has_wifi") == "on" else False
        cafe_has_sockets = True if request.form.get("has_sockets") == "on" else False
        cafe_can_take_calls = True if request.form.get("can_take_calls") == "on" else False
        cafe_coffee_price = "£"+request.form.get("coffee_price")

        new_cafe = Cafe(
            name=cafe_name,
            img_url=cafe_img_url,
            map_url=cafe_map_url,
            location=cafe_location,
            seats=cafe_seats,
            has_toilet=cafe_has_toilet,
            has_wifi=cafe_has_wifi,
            has_sockets=cafe_has_sockets,
            can_take_calls=cafe_can_take_calls,
            coffee_price=cafe_coffee_price
        )
        # Add the new cafe to the session
        db.session.add(new_cafe)
        # Commit the transaction to save the data in the database
        db.session.commit()
        return redirect(url_for("cafes"))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True, port=5004)
