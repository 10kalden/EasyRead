from flask import Flask, render_template, request, send_file
from botok import WordTokenizer
from botok.config import Config
from pathlib import Path
import os

app = Flask(__name__, template_folder='.')

def get_tokens(wt, text):
    tokens = wt.tokenize(text, split_affixes=False)
    return '  '.join(token['text'] for token in tokens)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tokenize', methods=['POST'])
def tokenize():
    config = Config(dialect_name='general', base_path=Path.home())
    wt = WordTokenizer(config=config)
    input_text = request.form['ipText']
    tokens = get_tokens(wt, input_text)
    output_text = "".join([str(token) for token in tokens])

    return render_template('index.html', input_text=input_text, output=output_text)

@app.route('/download_token', methods=['POST'])
def download_token():
    output_text = request.form['opText']
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(output_text)
    return send_file('output.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=os.getenv('FLASK_DEBUG', False))
