import os
from flask import Flask, render_template, request, flash, Response
from flask import get_flashed_messages, redirect, url_for
from .src import website
from requests import RequestException
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/')
def home_page() -> str:
    return render_template('index.html')


@app.post('/urls')
def add_url() -> str | Response:
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
    id, is_exists = website.add_new_site(site_name, app.config['DATABASE_URL'])
    if is_exists:
        flash('Страница уже существует', 'alert-info')
    else:
        flash('Страница успешно добавлена', 'alert-success')
    url = url_for('site_page', id=id)
    return redirect(url, code=302)


@app.get('/urls')
def list_sites() -> str:
    sites = website.get_all_sites(app.config['DATABASE_URL'])
    return render_template('list_sites.html', sites=sites)


@app.route('/urls/<int:id>')
def site_page(id: int) -> str:
    site, checks = website.get_site_and_checks(id, app.config['DATABASE_URL'])
    if not site:
        return render_template('404.html'), 404
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'site.html',
        messages=messages,
        site=site,
        checks=checks
    )


@app.post('/urls/<int:id>/checks')
def site_checks(id: int) -> str | Response:
    try:
        site = website.check_site(id, app.config['DATABASE_URL'])
        if not site:
            return render_template('404.html'), 404
    except RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
    else:
        flash('Страница успешно проверена', 'alert-success')
    url = url_for('site_page', id=id)
    return redirect(url, code=302)


@app.errorhandler(404)
def not_found(_):
    return render_template('404.html'), 404
