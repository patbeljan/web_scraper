from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

db = client.mars_db

db.table.drop()
db.weather.drop()
db.hemisphere.drop()
db.news.drop()
db.images.drop()

table_data = scrape_mars.mars_facts_table()
weather_data = scrape_mars.mars_weather()
hemisphere_data = scrape_mars.mars_hemisphere()
news_data = scrape_mars.mars_nasa_lastest_news()
images_data = scrape_mars.mars_images()

db.table.insert_one(table_data)
db.weather.insert_one(weather_data)
db.hemisphere.insert_many(hemisphere_data)
db.news.insert_one(news_data)
db.images.insert_one(images_data)

@app.route("/")
def index():

    table = db.table.find_one()
    weather = db.weather.find_one()
    hemisphere = db.hemisphere.find()
    news = db.news.find_one()
    images = db.images.find_one()

    # table = scrape_mars.mars_facts_table()
    # weather = scrape_mars.mars_weather()
    # hemisphere = scrape_mars.mars_hemisphere()
    # news = scrape_mars.mars_nasa_lastest_news()
    # images = scrape_mars.mars_images()

    return render_template("index.html", table = table, weather = weather, hemisphere = hemisphere, news = news, images = images)


@app.route("/scrape")
def scraper():

    db.table.drop()
    db.weather.drop()
    db.hemisphere.drop()
    db.news.drop()
    db.images.drop()

    table_data = scrape_mars.mars_facts_table()
    weather_data = scrape_mars.mars_weather()
    hemisphere_data = scrape_mars.mars_hemisphere()
    news_data = scrape_mars.mars_nasa_lastest_news()
    images_data = scrape_mars.mars_images()

    print(table_data)
    print(weather_data)
    print(hemisphere_data)
    print(news_data)
    print(images_data)

    db.table.insert_one(table_data)
    db.weather.insert_one(weather_data)
    db.hemisphere.insert_many(hemisphere_data)
    db.news.insert_one(news_data)
    db.images.insert_one(images_data)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(threaded = True, debug=True)
