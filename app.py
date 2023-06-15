from flask import Flask, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def text_preprocessing():
    data = request.get_json()

    text = data['text']

    tokens = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
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

    return jsonify({
        "Filtered Text: ": filtered_tokens,
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
