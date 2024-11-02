from code.retreive_and_answer import get_answer
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('input')
    # Simulate a response from a Q&A bot
    bot_response = f"You asked: {user_input}. Here's a quick answer!"
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
