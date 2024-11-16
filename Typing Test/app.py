from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# List of words for typing test
word_list = ["hello", "world", "python", "programming", "typing", "test", "keyboard", "screen", "functional", "highlight"]
score = 0

@app.route('/')
def index():
    global score
    word = random.choice(word_list)
    return render_template('index.html', word=word, score=score)

@app.route('/check_word/<typed_word>/<correct_word>', methods=['GET'])
def check_word(typed_word, correct_word):
    global score
    if typed_word == correct_word:
        score += 10  # Add points if the word is typed correctly
    return jsonify(score=score)

if __name__ == "__main__":
    app.run(debug=True)
