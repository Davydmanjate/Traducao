import os
import sys
import docx
import PyPDF2
import pyttsx3

def processar_documento(caminho_documento):
    texto = ""
    
    # Verificar a extensão do arquivo
    if caminho_documento.endswith('.pdf'):
        with open(caminho_documento, 'rb') as arquivo_pdf:
            leitor = PyPDF2.PdfReader(arquivo_pdf)
            for pagina in range(len(leitor.pages)):
                texto += leitor.pages[pagina].extract_text() or ""  # Adiciona texto extraído ou vazio se None
    elif caminho_documento.endswith('.docx'):
        doc = docx.Document(caminho_documento)
        for par in doc.paragraphs:
            texto += par.text + '\n'
    else:
        raise ValueError("Formato de documento não suportado. Utilize PDF ou DOCX.")
    
    return texto

def converter_texto_em_audio(texto, nome_arquivo):
    engine = pyttsx3.init()
    
    # Selecionar a voz em português, se disponível
    voz_encontrada = False
    for voz in engine.getProperty('voices'):
        if 'pt' in voz.languages or 'portuguese' in voz.name.lower():
            engine.setProperty('voice', voz.id)
            voz_encontrada = True
            break
    
    if not voz_encontrada:
        print("Aviso: Voz em português não encontrada. Usando voz padrão.")
    
    # Ajustar a velocidade da fala (opcional)
    engine.setProperty('rate', 200)  # 150 palavras por minuto (ajuste conforme necessário)
    
    # Salvar o áudio em um arquivo
    engine.save_to_file(texto, nome_arquivo)
    engine.runAndWait()
    print(f"Áudio salvo como {nome_arquivo}")

def main():
    if len(sys.argv) < 2:
        print("Erro: Caminho do documento não fornecido.")
        sys.exit(1)
    
    caminho_documento = sys.argv[1]
    if os.path.exists(caminho_documento):
        texto = processar_documento(caminho_documento)
        if texto.strip():
            nome_arquivo_audio = os.path.splitext(caminho_documento)[0] + '.mp3'
            converter_texto_em_audio(texto, nome_arquivo_audio)
        else:
            print("Erro: O documento está vazio ou não contém texto reconhecível.")
    else:
        print("Erro: Arquivo não encontrado.")

if __name__ == "__main__":
    main()
