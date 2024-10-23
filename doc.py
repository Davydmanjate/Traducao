import os
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
                texto += leitor.pages[pagina].extract_text()
    elif caminho_documento.endswith('.docx'):
        doc = docx.Document(caminho_documento)
        for par in doc.paragraphs:
            texto += par.text + '\n'
    else:
        raise ValueError("Formato de documento não suportado. Utilize PDF ou DOCX.")
    
    return texto

def converter_texto_em_audio(texto, nome_arquivo):
    engine = pyttsx3.init()
    
    # Salvar o áudio em um arquivo
    engine.save_to_file(texto, nome_arquivo)
    engine.runAndWait()
    print(f"Áudio salvo como {nome_arquivo}")

def main():
    caminho_documento = input("Digite o caminho do documento (PDF ou DOCX): ")
    
    if os.path.exists(caminho_documento):
        print("Arquivo encontrado.")
        texto = processar_documento(caminho_documento)
        print("Processando o arquivo...")
        
        # Nome do arquivo de áudio
        nome_arquivo_audio = os.path.splitext(caminho_documento)[0] + '.mp3'
        
        # Converter texto em áudio
        converter_texto_em_audio(texto, nome_arquivo_audio)
    else:
        print("Arquivo não encontrado.")

if __name__ == "__main__":
    main()
