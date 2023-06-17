from flask import Flask, request, jsonify
import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def text_preprocessing():
    data = request.get_json()

    text = data['text']

    tokens = word_tokenize(text)

    stop_words = set(["mightn't", 're','wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've",'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have',  'hasn', 'o', "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])

    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    tagged = nltk.pos_tag(tokens)

    tense = {"future": len([word for word in tagged if word[1] == "MD"]),
             "present": len([word for word in tagged if word[1] in ["VBP", "VBZ", "VBG"]]),
             "past": len([word for word in tagged if word[1] in ["VBD", "VBN"]]),
             "present_continuous": len([word for word in tagged if word[1] in ["VBG"]])}

    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    temp = []
    for w in lemmatized_tokens:
        if w == 'I':
            temp.append('Me')
        else:
            temp.append(w)
    words = temp
    probable_tense = max(tense, key=tense.get)

    if probable_tense == "past" and tense["past"] >= 1:
        temp = ["Before"]
        temp = temp + words
        words = temp
    elif probable_tense == "future" and tense["future"] >= 1:
        if "Will" not in words:
            temp = ["Will"]
            temp = temp + words
            words = temp
        else:
            pass
    elif probable_tense == "present":
        if tense["present_continuous"] >= 1:
            temp = ["Now"]
            temp = temp + words
            words = temp

        # generate sign language animationsGit push origin main
    animations = []
    for word in filtered_tokens:
        path = f"assets/{word}.mp4"
        f = os.path.exists(path)
        if not f:
            for c in word:
                animations.append(c)
        else:
            animations.append(word)

    return jsonify({'animations': animations}), 200


if __name__ == '__main__':
    app.run(debug=True)
