from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_nasa

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/nasa"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars = mongo.db.marsnews.find()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    mars = mongo.db.marsnews
    mars_data = scrape_nasa.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
