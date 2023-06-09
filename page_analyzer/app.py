from flask import Flask, render_template, request, redirect, url_for, flash, \
    get_flashed_messages
from page_analyzer import db
import validators
from urllib.parse import urlparse
import requests
from page_analyzer.db import get_info_by_id
import bs4

app = Flask(__name__)
app.secret_key = 'super secret key'


def lencheck(arr):
    if arr:
        arr = arr.text
        if len(arr) >= 255:
            return "is too long, >254"
        else:
            return str(arr)
    else:
        return ""


def check_transformation(data):
    all = []
    for i in sorted(data, key=lambda x: x[0], reverse=True):
        ans = {"id": i[0], "status_code": i[1],
               "created_at": i[2].strftime("%d/%m/%Y"), "h1": i[3],
               "title": i[4], "description": i[5]}
        all.append(ans)
    return all


def transform(urls):
    new_urls = []
    for url in sorted(urls, key=lambda x: x[0], reverse=True):
        if url[3]:
            new_urls.append(
                {"id": url[0], "name": url[1], "status_code": url[3],
                 "last_check": url[4].strftime("%d/%m/%Y")})
        else:
            new_urls.append(
                {"id": url[0], "name": url[1]})
    return new_urls


def transform_user(url):
    new_url = {"id": url[0], "name": url[1],
               "created_at": url[2].strftime("%d/%m/%Y")}
    return new_url


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    if request.method == 'POST':
        try:
            url_site = request.form['url']
            parsed_url = urlparse(url_site)
            norm_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
        except KeyError:
            flash("Некорректный URL", "alert-danger")
            return render_template('index.html',
                                   messages=get_flashed_messages(
                                       with_categories=True))
        if validators.url(norm_url):
            if db.get_id_by_name(norm_url):
                flash("Страница уже существует", "alert-info")
            else:
                flash("Страница успешно добавлена", "alert-success")
                db.add_site(norm_url)
            site_id = db.get_id_by_name(norm_url)
            return redirect(url_for('site', site_id=site_id))
        else:
            flash("Некорректный URL", "alert-danger")
            return render_template('index.html',
                                   messages=get_flashed_messages(
                                       with_categories=True)), 422
    urls = transform(db.all_sites())
    return render_template('urls.html', urls=urls,
                           messages=get_flashed_messages(
                               with_categories=True))


@app.route('/urls/<int:site_id>')
def site(site_id):
    site = db.get_site(site_id)
    if site:
        site = transform_user(site)
        info = check_transformation(get_info_by_id(site_id))
        return render_template('site.html', url=site, checks=info,
                               messages=get_flashed_messages(
                                   with_categories=True))
    else:
        flash("Site not found", "alert-danger")
        return render_template('index.html', messages=get_flashed_messages(
            with_categories=True))


@app.route('/urls/<int:site_id>/checks', methods=['POST'])
def check(site_id):
    try:
        request_data = requests.get(db.get_site(site_id)[1])
        status = request_data.status_code
        if status != 200:
            flash("Произошла ошибка при проверке", "alert-danger")
            return redirect(url_for('site', site_id=site_id))
        out = bs4.BeautifulSoup(request_data.text, 'html.parser')
        h1 = lencheck(out.find('h1'))
        title = lencheck(out.find('title'))
        description = (
            out.find("meta", attrs={"name": 'description'}))
        if description:
            description = description['content'].strip()
        db.add_check(site_id, status, h1, title, description)
        flash("Страница успешно проверена", "alert-success")
        return redirect(url_for('site', site_id=site_id))
    except requests.RequestException:
        flash("Произошла ошибка при проверке", "alert-danger")
        return site(site_id)


if __name__ == '__main__':
    app.run()
