import logging
import os
import validators
from flask import Flask, render_template, request, flash
from flask import get_flashed_messages, redirect, url_for
from dotenv import load_dotenv
from .src import website
from .src import from_db

log = logging.getLogger(__name__)

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def validate(site_name: str) -> tuple:
    if len(site_name) > 255:
        return ('URL превышает 255 символов', 'alert-danger')
    if not validators.url(site_name):
        return ('Некорректный URL', 'alert-danger')
    return ()


@app.route('/')
def home_page() -> str:
    return render_template('index.html')


@app.post('/urls')
def add_url() -> str:
    site_name = request.form.get('url', '', str)
    error = validate(site_name)
    if error:
        flash(*error)
        messages = get_flashed_messages(with_categories=True)
        # В примере не спрашивает про повторную отправку формы
        return render_template(
            'index.html',
            messages=messages,
            site_name=site_name
        ), 422
    id = website.get_site_id(site_name, from_db)
    if id is None:
        id = website.add_site(site_name, from_db)
        flash('Страница успешно добавлена', 'alert-success')
    else:
        flash('Страница уже существует', 'alert-info')
    url = url_for('site_page', id=id)
    return redirect(url, code=302)


@app.get('/urls')
def list_sites() -> str:
    sites = website.get_all_site(from_db)
    return render_template('list_sites.html', sites=sites)


@app.get('/urls/<id>')
def site_page(id: str) -> str:
    site = website.get_site(int(id), from_db)
    if not site:
        return render_template('404.html'), 404
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'site.html',
        messages=messages,
        site=site
    )
