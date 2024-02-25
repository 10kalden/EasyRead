from flask import Flask, render_template, request, send_file, url_for
from botok import WordTokenizer
from botok.config import Config
from pathlib import Path

app = Flask(__name__, template_folder='.')

def tokenize_text(text):
    config = Config(dialect_name='general', base_path=Path.home())
    wt = WordTokenizer(config=config)
    try:
        tokens = wt.tokenize(text, split_affixes=False)
        return '  '.join(token['text'] for token in tokens), None
    except Exception as e:
        return None, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tokenize', methods=['POST'])
def tokenize():
    input_text = request.form.get('ipText', '')
    if not input_text:
        error_message = "Input text is required."
        return render_template('index.html', error=error_message)

    output_text, error = tokenize_text(input_text)
    if error:
        return render_template('index.html', input_text=input_text, error=error)

    return render_template('index.html', input_text=input_text, output=output_text)

@app.route('/download_token', methods=['POST'])
def download_token():
    output_text = request.form.get('opText', '')
    if not output_text:
        error_message = "No tokenized text to download."
        return render_template('index.html', error=error_message)

    try:
        with open('output.txt', 'w', encoding='utf-8') as file:
            file.write(output_text)
        return send_file('output.txt', as_attachment=True)
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
