from flask import Flask, request, render_template, send_file
from googletrans import Translator
from gtts import gTTS
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_file():
    if 'file' not in request.files:
        return "Nenhum arquivo enviado", 400
    
    file = request.files['file']
    if file.filename == '':
        return "Arquivo inválido", 400
    
    lang = request.form.get('lang')
    if not lang:
        return "Idioma não selecionado", 400

    # Salvar o arquivo enviado
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Ler o texto do arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Traduzir o texto
    translator = Translator()
    translated = translator.translate(text, dest=lang)
    translated_text = translated.text

    # Converter o texto traduzido em áudio
    tts = gTTS(translated_text, lang=lang)
    audio_path = os.path.join(OUTPUT_FOLDER, f"{file.filename.split('.')[0]}_{lang}.mp3")
    tts.save(audio_path)

    return send_file(audio_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
