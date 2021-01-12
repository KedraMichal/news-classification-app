import json
import nltk
import numpy as np
import keras
from stempel import StempelStemmer
from data_for_model import clear_json
import requests


def article_coding(text, input_words):
    if text is None:
        text = ""
    text = text.lower()
    text = nltk.wordpunct_tokenize(text)
    text = [stemmer.stem(word) for word in text]

    coded_sentence = []
    for w in input_words:
        if w in text:
            coded_sentence.append(1)
        else:
            coded_sentence.append(0)

    return np.asarray(coded_sentence).reshape(1, -1)


def modify_app_database(file_name, model, input_words, output_categories, update=False):
    if update is False:
        database = {'articles': []}
    else:
        with open(file_name, 'r', errors="ignore") as outfile:
            database = json.load(outfile)

    r = requests.get(
        'http://newsapi.org/v2/top-headlines?country=pl&pageSize=100&apiKey=4dbe844f205e480aab6d9ee818ca6019')
    data = r.json()
    data = data['articles']
    for article in data:
        text = article_coding(article['description'], input_words)
        if np.max(model.predict(text)) > 0.5:
            chosen_category_index = np.argmax(model.predict(text))
            chosen_category = output_categories[chosen_category_index]
        else:
            chosen_category = "Pozostałe"

        database['articles'].append(
            {'title': article['title'], 'category': chosen_category, 'description': article['description'],
             'url': article['url'], "urlimage": article['urlToImage'], "date": article['publishedAt']})

    with open(file_name, 'w', errors='ignore') as outfile:
        json.dump(database, outfile, ensure_ascii=False, indent=2)

    clear_json(file_name)


stemmer = StempelStemmer.default()
main_model = keras.models.load_model("resources/generated/model.h5")
with open('resources/generated/input_layer_words.txt', 'r') as words:
    input_layer_words = json.load(words)
output_layer_categories = ['Sport', 'Zdrowie', 'Biznes', 'Rozrywka', 'Technologie']

#modify_app_database("resources/app_data.json", main_model, input_layer_words, output_layer_categories, True)
# modify_app_database("rss2s.json", main_model, input_layer_words, output_layer_categories, True)
