from flask import Flask, render_template, request, redirect, url_for, \
    get_flashed_messages
from page_analyzer import db

app = Flask(__name__)


def transform(urls):
    new_urls = []
    for url in urls:
        new_urls.append(
            {"id": url[0], "name": url[1]})
    return new_urls


def transform_user(url):
    new_url = {"id": url[0], "name": url[1],
               "created_at": url[2].strftime("%d/%m/%Y")}
    return new_url


def validate_url(url):
    if not (url.startswith('http://') or url.startswith('https://')):
        return False
    if url == '':
        return False
    return True


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    if request.method == 'POST':
        try:
            url_site = request.form['url']
        except KeyError:
            return render_template('index.html',
                                   messages=[("danger",
                                              "Please enter a valid URL")])
        if validate_url(url_site):
            db.add_site(request.form)
        else:
            return render_template('index.html',
                                   messages=[("danger",
                                              "Please enter a valid URL")])
        return redirect(url_for('urls'))
    urls = transform(db.all_sites())
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:site_id>')
def site(site_id):
    try:
        site = transform_user(db.get_site(site_id))
        return render_template('site.html', url=site,
                               messages=get_flashed_messages())
    except:
        return render_template('site.html', messages=[("danger",
                                                       "Site not found")])


def get_site(site_id):
    return render_template('site.html', site=db.get_site(site_id))


if __name__ == '__main__':
    app.run()
