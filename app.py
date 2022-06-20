# Import flask, PyMongo, and scraping code
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Home route
@app.route("/")
def index():
    # Uses PyMongo to find the mars collection in our database
    mars = mongo.db.mars.find_one()
    # tells Flask to return html template and use mars collection
    return render_template("index.html", mars=mars)

# Route will scrape updated data
@app.route("/scrape")
def scrape():
    # variable points to mongo db
    mars = mongo.db.mars
    # holds newly scraped data
    mars_data = scraping.scrape_all()
    # insert data into mongo db
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    # navigate back to homepage
    return redirect('/', code=302)

# Tell flask to run
if __name__ == "__main__":
   app.run()