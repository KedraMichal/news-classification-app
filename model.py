import json
import nltk
import numpy as np
import keras
from sklearn.model_selection import train_test_split
from stempel import StempelStemmer


np.set_printoptions(suppress=True)


with open('resources/generated/news_data.json', 'r') as f:
    data = json.load(f)

all_words = []
all_articles = []
all_categories = []

for article in data['articles']:
    art = str(article['description']).lower()
    tokens = nltk.wordpunct_tokenize(art)
    all_words.extend(tokens)
    all_articles.append(art.lower())
    all_categories.append(article['category'])

stemmer = StempelStemmer.default()
all_words = [stemmer.stem(word) for word in all_words]

all_words = list(set(all_words))
all_words.remove(None)
all_words = sorted(all_words)

with open('resources/generated/input_layer_words.txt', 'w') as datafile:
    json.dump(all_words, datafile)

unique_categories = ['sports', 'health', 'business', 'entertainment', 'technology']

x = []
y = []

for article in all_articles:
    used_words = []
    article_words = nltk.wordpunct_tokenize(article)
    article_words = [stemmer.stem(word) for word in article_words]
    for word in all_words:
        if word in article_words:
            used_words.append(1)
        else:
            used_words.append(0)

    x.append(used_words)

for category in all_categories:
    row = [0] * len(unique_categories)
    category_number = unique_categories.index(category)
    row[category_number] = 1

    y.append(row)

x = np.asarray(x)
y = np.asarray(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.7)
# #
#
# model = keras.models.Sequential()
# model.add(keras.layers.Dense(32, input_shape=[len(all_words)], activation='relu'))
# model.add(keras.layers.Dense(32, activation='relu'))
# model.add(keras.layers.Dense(len(unique_categories), activation='softmax'))
#
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# model.fit(x_train, y_train, epochs=20)
# model.save("model.h5")

model = keras.models.load_model("resources/generated/model.h5")
#
predicted = model.predict_classes(x_test)
sum_test_y = len(predicted)
predicted_correct = 0
distr = model.predict(x_test)
for i in range(len(predicted)):

    print(predicted[i], np.argmax(y_test[i, :]))
    print(distr[i, :])
    if predicted[i] == np.argmax(y_test[i, :]):  # argmax z [[0 0 0 0 1 0]]
        predicted_correct += 1
print(unique_categories)
print(predicted_correct / sum_test_y)


