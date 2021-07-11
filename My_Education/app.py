from flask import Flask, render_template, request
import numpy as np

import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from bs4 import BeautifulSoup
import requests

from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)


count_vect = CountVectorizer()

rawdf = pd.read_csv('UniData.csv')
df = pd.read_csv('UniData.csv')

X_train = df['Description']
count_vect.fit_transform(X_train)

@app.route("/")
def index():
    uniques = df.Topic.dropna().unique()
    uniques = np.append(uniques, "all")
    fixeduniq = []
    length = len(uniques)
    for x in uniques:
        fixeduniq.append(x.replace(" ","_"))
    print(fixeduniq)

    return render_template('index.html',topics=fixeduniq,viewtopics=uniques,len=length)

def getmodel(topic):
    df = pd.read_csv('UniData.csv')

    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2',
                            encoding='latin-1', ngram_range=(1, 2),
                            stop_words='english')
    features = tfidf.fit_transform(df.Description).toarray()
    labels = df.Uni
    if topic != "all":
        extra = df.iloc[-1]
        df = rawdf.loc[df.Topic == topic]
        df = df.append(extra)


    X_train = df['Description']
    y_train = df['Uni']
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    clf = LinearSVC(C=2).fit(X_train_tfidf.toarray(), y_train)
    return clf

@app.route("/predict", methods=['POST'])
def prediction():
    if request.method == 'POST':
        data = request.form['a']
        topicdata = request.form['b'].replace('_'," ")
        print(topicdata)
        model = getmodel(topicdata)
        prediction = model.predict(count_vect.transform([data]).toarray())

        search = prediction[0].capitalize().replace(" ","_")
        source = requests.get(f'https://en.wikipedia.org/wiki/{search}').text
        soup = BeautifulSoup(source, 'lxml')
        main = soup.find(id="mw-content-text")
        main.find('p').decompose()
        content = main.find('p')

        cleanedcontent = content.text.replace("[","").replace("]","").replace("1","").replace("2","")\
              .replace("3","").replace("4","").replace("5","").replace("6","").replace("7","")\
              .replace("8","").replace("9","").replace("0","")
        if prediction[0] == "nothing":
            cleanedcontent = ""
        return render_template('prediction.html',data=prediction[0].capitalize(),info=cleanedcontent)
    else :
        return render_template('prediction.html')

if __name__ == '__main__':
    app.run(debug=True)