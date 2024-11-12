import os
import wave
import json
import vosk
import sounddevice as sd
import queue
import time

def gerar_nome_arquivo(base_dir=".", prefixo="gravacao", extensao=".wav"):
    """Gera um nome de arquivo único com numeração sequencial."""
    numero = 1
    while True:
        nome_arquivo = os.path.join(base_dir, f"{prefixo}_{numero}{extensao}")
        if not os.path.exists(nome_arquivo):
            return nome_arquivo
        numero += 1

def salvar_texto(texto, caminho_arquivo):
    """Salva o texto em um arquivo .txt."""
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(texto)
    print(f"Texto salvo em {caminho_arquivo}")

def reconhecer_fala():
    modelo_path = "./vosk-small"
    if not os.path.exists(modelo_path):
        raise Exception(f"Modelo Vosk não encontrado no caminho: {modelo_path}. Verifique se o modelo está na pasta 'vosk-small'.")

    modelo = vosk.Model(modelo_path)
    print("Modelo carregado com sucesso!")

    samplerate = 16000
    q = queue.Queue()

    # Gerar nome único para o arquivo de gravação
    nome_arquivo_audio = gerar_nome_arquivo(prefixo="gravacao", extensao=".wav")
    wf = wave.open(nome_arquivo_audio, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(samplerate)

    def callback(indata, frames, time, status):
        if status:
            print(f"Erro de status de áudio: {status}")
        q.put(bytes(indata))
        wf.writeframes(indata)

    texto_final = []
    tempo_inicial = time.time()
    duracao_maxima = 60  # Limite de gravação

    try:
        with sd.RawInputStream(samplerate=samplerate, blocksize=4096, dtype='int16', channels=1, callback=callback):
            print("Gravando... Pressione Ctrl+C para parar.")
            reconhecedor = vosk.KaldiRecognizer(modelo, samplerate)

            while True:
                if time.time() - tempo_inicial > duracao_maxima:
                    print("Tempo limite atingido. Finalizando...")
                    break

                data = q.get()
                if reconhecedor.AcceptWaveform(data):
                    resultado = reconhecedor.Result()
                    resultado_json = json.loads(resultado)
                    texto_final.append(resultado_json.get('text', ''))
                    print(f"Texto reconhecido até agora: {' '.join(texto_final)}")
                else:
                    print("Resultado parcial:", reconhecedor.PartialResult())

    except KeyboardInterrupt:
        print("\nGravação interrompida pelo usuário.")
    except Exception as e:
        print(f"Erro durante a captura de áudio: {str(e)}")
    finally:
        wf.close()
        print(f"Arquivo de áudio salvo como '{nome_arquivo_audio}'.")

    # Salvar o texto em um arquivo .txt
    nome_arquivo_texto = os.path.splitext(nome_arquivo_audio)[0] + ".txt"
    salvar_texto(' '.join(texto_final), nome_arquivo_texto)

    return ' '.join(texto_final)

def main():
    try:
        texto = reconhecer_fala()
        print(f"Texto final reconhecido: {texto}")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()
