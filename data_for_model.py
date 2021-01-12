import requests
import json


def make_json(filename, update=False):
    if update is False:
        json_to_update = {'articles': []}
    else:
        with open(filename, 'r', errors="ignore") as outfile:
            json_to_update = json.load(outfile)

    categories = ['sports', 'health', 'business', 'entertainment', 'technology']
    for i in categories:
        r = requests.get(
            'http://newsapi.org/v2/top-headlines?country=pl&category={}&pageSize=100&apiKey=4dbe844f205e480aab6d9ee818ca6019'.format(
                i))
        data_to_add = r.json()
        data_to_add = data_to_add['articles']
        for article in data_to_add:
            json_to_update['articles'].append(
                {'title': article['title'], 'category': i, 'description': article['description'], 'publishedAt': article['publishedAt'],
                 'url': article['url']})

    with open(filename, 'w', errors='ignore') as outfile:
        json.dump(json_to_update, outfile, indent=2)

    clear_json(filename)


def remove_duplicates_from_list(alist):
    list_without_duplicates = []
    for i in alist:
        if i not in list_without_duplicates:
            list_without_duplicates.append(i)

    return list_without_duplicates


def clear_json(filename):
    with open(filename, 'r', errors="ignore") as outfile:
        json_to_update = json.load(outfile)

    json_to_update['articles'] = remove_duplicates_from_list(json_to_update['articles'])
    none_descriptions = []
    for i in json_to_update['articles']:
        if i['description'] is None:
            none_descriptions.append(i)
    for i in none_descriptions:
        json_to_update['articles'].remove(i)

    for article in json_to_update['articles'].copy():
        if len(article['description']) < 175:
            json_to_update['articles'].remove(article)

    with open(filename, "w", errors='ignore') as outfile:
        json.dump(json_to_update, outfile, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # make_json("news_data.json", False)
    make_json("resources/generated/news_data.json", True)


