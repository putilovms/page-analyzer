from flask import Flask, render_template, url_for
import os
from dotenv import load_dotenv
import logging
import psycopg2

custom_time_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(
    level=logging.DEBUG,
    filename="page_analyzer.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt=custom_time_format
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
logging.debug(f"Коннект к БД: {conn}")


@app.route('/')
def home_page():
    url = url_for('home_page')
    logging.debug(f"Страница загружена: {url}")
    return render_template('index.html')
