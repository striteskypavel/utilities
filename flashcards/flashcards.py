from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Slovník slovíček
flashcards = {
    'apple': 'jablko',
    'dog': 'pes',
    'house': 'dům',
    'book': 'kniha',
    'car': 'auto',
    'computer': 'počítač',
    'water': 'voda',
    'sun': 'slunce',
    'moon': 'měsíc',
    'tree': 'strom'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_word')
def get_word():
    word = random.choice(list(flashcards.keys()))
    return jsonify({'word': word})

@app.route('/get_translation', methods=['POST'])
def get_translation():
    word = request.json.get('word')
    translation = flashcards.get(word, '')
    return jsonify({'translation': translation})

if __name__ == '__main__':
    app.run(debug=True)
