from flask import Flask, request, jsonify, render_template
import pickle
import re
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import gunicorn
nltk.download('punkt_tab')

app = Flask(__name__)

try:
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)

    with open('vectorizer.pkl', 'rb') as file:
        vectorizer = pickle.load(file)
except:
    print("Error loading model or vectorizer files")

def clear_text(text):
    text = str(text).lower()
    text = re.sub('<.*?>', '', text)
    text = re.sub('http\S+|https\S+|www\S+', '', text)
    text = re.sub('@\S+|#\S+', '', text)
    text = re.sub('[^\w\s]', '', text)
    tokens = word_tokenize(text)
    return ' '.join(tokens)

def predict_sentiment(input_text, model, vectorizer):
    try:
        cleaned_text = clear_text(input_text)
        input_vector = vectorizer.transform([cleaned_text]).toarray()
        prediction = model.predict(input_vector)
        sentiment = prediction[0]
        
        if sentiment in ['negative', 'neutral', 'positive']:
            return sentiment.capitalize()
        else:
            print(f"Unexpected prediction value: {sentiment}")
            return "Prediction Error"
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid input, provide text for prediction'}), 400
    raw_text = data['text']
    
    if model is None or vectorizer is None:
        return jsonify({'error': 'Model or vectorizer not loaded properly'}), 500
    
    sentiment = predict_sentiment(raw_text, model, vectorizer)
    
    if sentiment is None:
        return jsonify({'error': 'Prediction failed, please try again'}), 500
    
    return jsonify({'sentiment': sentiment})

if __name__ == '__main__':
    app.run(debug=True)
