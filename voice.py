import os
import sys
import wave
import json
import vosk
import pyaudio
import sounddevice as sd
import queue

def reconhecer_fala(modelo_path):
    if not os.path.exists(modelo_path):
        raise Exception(f"Modelo não encontrado no caminho: {modelo_path}")

    try:
        modelo = vosk.Model(modelo_path)
        print("Modelo carregado com sucesso!")
    except Exception as e:
        raise Exception(f"Erro ao carregar o modelo: {str(e)}")

    samplerate = 16000  # Taxa de amostragem de áudio
    q = queue.Queue()

    # Gravar áudio em um arquivo
    wf = wave.open("gravacao.wav", "wb")
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 16 bits
    wf.setframerate(samplerate)

    def callback(indata, frames, time, status):
        if status:
            print(f"Erro de status de áudio: {status}")
        q.put(bytes(indata))
        wf.writeframes(indata)  # Salvar o áudio

    try:
        # Aumentar o volume do microfone, se necessário
        with sd.RawInputStream(samplerate=samplerate, blocksize=8192, dtype='int16', channels=1, callback=callback):
            print("Gravando... Pressione Ctrl+C para parar.")
            reconhecedor = vosk.KaldiRecognizer(modelo, samplerate)

            while True:
                data = q.get()
                if reconhecedor.AcceptWaveform(data):
                    resultado = reconhecedor.Result()
                    resultado_json = json.loads(resultado)
                    print(f"Texto reconhecido: {resultado_json.get('text', '')}")
                    return resultado_json.get('text', '')
                else:
                    print(reconhecedor.PartialResult())

    except Exception as e:
        print(f"Erro durante a captura de áudio: {str(e)}")
    finally:
        wf.close()  # Fechar o arquivo de áudio ao final

def main():
    modelo_path = input("Digite o caminho do diretório do modelo Vosk (por exemplo, vosk-model-small-pt-0.3): ")
    print(f"Usando o modelo no caminho: {modelo_path}")

    try:
        texto = reconhecer_fala(modelo_path)
        print(f"Texto final reconhecido: {texto}")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()
