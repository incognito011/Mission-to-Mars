# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_dict = mongo.db.collection.find_one()
   
    # print(mars_dict)
    # return template and data
    return render_template("index.html", mars_dict=mars_dict)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    
    news = scrape_mars.scrape_news()
    print("finished news")
    jpl = scrape_mars.scrape_jpl()
    print("finished jpl")
    weather = scrape_mars.scrape_weather()
    print("finished weather")
    facts = scrape_mars.scrape_facts()
    print("finished facts")
    hemi = scrape_mars.scrape_hemisphere()
    print("finished hemi")
    
    # Store results into a dictionary
    mars_dict = {
        "news_title": news["news_title"],
        "news_p": news["news_p"],
        "featured_image_url": jpl["featured_image_url"],
        "mars_weather": weather["mars_weather"],
        "mars_facts": facts["mars_facts"],
        "mars_hemisphere": hemi["mars_hemisphere"],
    }
    # Remove old record
    mongo.db.collection.remove({})
    # Insert forecast into database
    mongo.db.collection.insert_one(mars_dict)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
