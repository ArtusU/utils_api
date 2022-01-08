from flask import Flask

from logger import trigger_log_save
from scrape import run as scrape_runner

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello_world():
    return "Hello, world. this is Flask"


@app.route("/box-office-mojo-scraper", methods=['POST'])
def box_office_scraper_view():
    trigger_log_save()
    scrape_runner()
    return {"data": [1,2,3]}