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

@app.route('/converter_audio', methods=['POST'])
def converter_audio():
    if 'documento' not in request.files:
        return "Nenhum arquivo enviado", 400
    
    file = request.files['documento']
    if file.filename == '':
        return "Arquivo inválido", 400
    
    lang = request.form.get('lang')
    if not lang:
        return "Idioma não selecionado", 400

    # Salvar o arquivo enviado
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Ler o texto do arquivo
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        return f"Erro ao ler o arquivo: {str(e)}", 400

    # Traduzir o texto
    try:
        translator = Translator()
        translated = translator.translate(text, dest=lang)
        translated_text = translated.text
    except Exception as e:
        return f"Erro na tradução: {str(e)}", 400

    # Converter o texto traduzido em áudio
    try:
        tts = gTTS(translated_text, lang=lang)
        audio_path = os.path.join(OUTPUT_FOLDER, f"{file.filename.split('.')[0]}_{lang}.mp3")
        tts.save(audio_path)
    except Exception as e:
        return f"Erro ao gerar o áudio: {str(e)}", 400

    return send_file(audio_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
