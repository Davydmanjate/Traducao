from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/converter_audio', methods=['POST'])
def converter_audio():
    documento = request.files['documento']
    if documento:
        caminho_documento = os.path.join('uploads', documento.filename)
        documento.save(caminho_documento)
        
        # Chama o script doc.py para converter documento em áudio
        subprocess.run(['python', 'doc.py', caminho_documento])  # Adapte conforme necessário

        return f"Áudio criado a partir do documento {documento.filename}!"
    return "Nenhum documento enviado."

@app.route('/captar_fala', methods=['POST'])
def captar_fala():
    # Chama o script voice.py para capturar fala e converter em texto
    subprocess.run(['python', 'voice.py'])  # Adapte conforme necessário

    return "Áudio capturado e convertido em texto!"

if __name__ == '__main__':
    app.run(debug=True)
