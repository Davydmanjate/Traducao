from flask import Flask, render_template, request
import os
import subprocess
import threading
import pyttsx3
import PyPDF2

app = Flask(__name__)

# Configuração da pasta de upload
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

def executar_script(script, *args):
    """Função para executar scripts de conversão em uma nova thread."""
    subprocess.run(['python', script, *args])

@app.route('/converter_audio', methods=['POST'])
def converter_audio():
    documento = request.files['documento']
    if documento:
        caminho_documento = os.path.join(app.config['UPLOAD_FOLDER'], documento.filename)
        documento.save(caminho_documento)
        
        # Executa o script doc.py em uma nova thread para conversão em áudio
        threading.Thread(target=executar_script, args=('doc.py', caminho_documento)).start()
        
        return f"Conversão em áudio iniciada para o documento {documento.filename}!"
    return "Nenhum documento enviado."

@app.route('/captar_fala', methods=['POST'])
def captar_fala():
    # Executa o script voice.py em uma nova thread para captura de fala
    threading.Thread(target=executar_script, args=('voice.py',)).start()
    
    return "Captura de áudio e conversão em texto iniciadas!"

if __name__ == '__main__':
    app.run(debug=True)
