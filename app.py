from flask import Flask, render_template, request, url_for
import json
from flask_bootstrap import Bootstrap
from datetime import datetime
import predict as p

app = Flask(__name__)
Bootstrap(app)


with open('resources/app_data.json', 'r') as f:
    data = json.load(f)
data = data['articles']
for i in data:
    i['date'] = datetime.strptime(i['date'], "%Y-%m-%dT%H:%M:%SZ")


@app.route('/')
@app.route('/home')
def home():
    return render_template('main.html', data=data)


@app.route('/info')
def info():
    my_var = request.args.get('my_var', None)
    for art in data:
        if art['title'] == my_var:
            my_var = art
            break

    return render_template('article.html', article=my_var)


@app.route('/date_sort')
def date_sort():
    actual_cat = request.args.get('category', None)
    if actual_cat and actual_cat != "Pozostałe":
        category_data = []
        for art in data:
            if art['category'] == actual_cat:
                category_data.append(art)
        sorted_data = sorted(category_data, key=lambda k: k['date'])

    elif actual_cat == "" or actual_cat == "Pozostałe":
        sorted_data = sorted(data, key=lambda k: k['date'])

    return render_template('main.html', data=sorted_data, actual_category=actual_cat)


@app.route('/date_sort2')
def date_sort2():
    actual_cat = request.args.get('category', None)
    if actual_cat and actual_cat != "Pozostałe":
        category_data = []
        for art in data:
            if art['category'] == actual_cat:
                category_data.append(art)
        sorted_data = sorted(category_data, key=lambda k: k['date'], reverse=True)

    elif actual_cat == "" or actual_cat == "Pozostałe":
        sorted_data = sorted(data, key=lambda k: k['date'], reverse=True)

    return render_template('main.html', data=sorted_data, actual_category=actual_cat)


@app.route('/update')
def update():
    p.modify_app_database("resources/app_data.json", p.main_model, p.input_layer_words, p.output_layer_categories, True)
    with open('resources/app_data.json', 'r') as f:
        data = json.load(f)
    data = data['articles']
    for i in data:
        i['date'] = datetime.strptime(i['date'], "%Y-%m-%dT%H:%M:%SZ")

    return render_template('main.html', data=data)


@app.route('/category')
def category():
    new_data = []
    chosen_category = request.args.get('category', None)
    for art in data:
        if art['category'] == chosen_category:
            new_data.append(art)

    return render_template('main.html', data=new_data, actual_category=chosen_category)


if __name__ == "__main__":
    app.run()
