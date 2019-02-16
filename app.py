from flask import Flask, render_template, redirect
#from flask_pymongo import PyMongo
#from flask import Markup
import scrape_mars
import pymongo

app = Flask(__name__)
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
db = client.mars_db



@app.route("/")
def index():
    qdata= db.mars.find_one()
    subset_hemis = {k:v for k,v in qdata.items() if k.endswith('Enhanced') }
    return render_template("index.html", mdata=qdata, hemis=subset_hemis)


@app.route("/scrape")
def scraper():
    #mars = mongo.db.mars_db
    mdata = scrape_mars.scrape()
    db.mars.update({}, mdata, upsert=True)
    
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
