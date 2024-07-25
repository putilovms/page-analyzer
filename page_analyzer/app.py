import logging
import os

from flask import Flask, render_template, request, flash, Response
from flask import get_flashed_messages, redirect, url_for
from dotenv import load_dotenv
from .src import website
from typing import Union
from requests import get, RequestException

log = logging.getLogger(__name__)

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/')
def home_page() -> str:
    return render_template('index.html')


@app.post('/urls')
def add_url() -> Union[str, Response]:
    site_name = request.form.get('url', '', str)
    error = website.validate(site_name)
    if error:
        flash(error, 'alert-danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            messages=messages,
            site_name=site_name
        ), 422
    id, is_exists = website.get_id_or_add(site_name)
    if is_exists:
        flash('Страница уже существует', 'alert-info')
    else:
        flash('Страница успешно добавлена', 'alert-success')
    url = url_for('site_page', id=id)
    return redirect(url, code=302)


@app.get('/urls')
def list_sites() -> str:
    sites = website.get_all_sites()
    return render_template('list_sites.html', sites=sites)


@app.route('/urls/<id>')
def site_page(id: str) -> str:
    site = website.get_site(int(id))
    if not site:
        return render_template('404.html'), 404
    checks = website.get_checks(int(id))
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'site.html',
        messages=messages,
        site=site,
        checks=checks
    )


@app.post('/urls/<id>/checks')
def site_checks(id: str) -> Union[str, Response]:
    site = website.get_site(int(id))
    if not site:
        return render_template('404.html'), 404
    try:
        response = get(site.name)
        response.raise_for_status()
        website.check_site(int(id), response)
    except RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
    else:
        flash('Страница успешно проверена', 'alert-success')
    url = url_for('site_page', id=id)
    return redirect(url, code=302)
