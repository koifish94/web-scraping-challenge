# MongoDB and Flask Application


from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def home():

    mars_record = mongo.db.collection.find_one()

    return render_template("index.html", mars=mars_record)


@app.route("/scrape")
def scrape():

    
    mars_data = scrape_mars.scrape()
    

    mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
