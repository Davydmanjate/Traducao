import os
import wave
import json
import vosk
import sounddevice as sd
import queue
import time

def reconhecer_fala():
    modelo_path = "./vosk-small"
    if not os.path.exists(modelo_path):
        raise Exception(f"Modelo Vosk não encontrado no caminho: {modelo_path}. Verifique se o modelo está na pasta 'vosk-small'.")

    modelo = vosk.Model(modelo_path)
    print("Modelo carregado com sucesso!")

    samplerate = 16000
    q = queue.Queue()

    wf = wave.open("gravacao.wav", "wb")
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
    duracao_maxima = 30  # Limite de gravação

    try:
        with sd.RawInputStream(samplerate=samplerate, blocksize=40960, dtype='int16', channels=1, callback=callback):
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
                    print(reconhecedor.PartialResult())

    except KeyboardInterrupt:
        print("\nGravação interrompida pelo usuário.")
    except Exception as e:
        print(f"Erro durante a captura de áudio: {str(e)}")
    finally:
        wf.close()
        print("Arquivo de áudio salvo como 'gravacao.wav'.")

    return ' '.join(texto_final)

def main():
    try:
        texto = reconhecer_fala()
        print(f"Texto final reconhecido: {texto}")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()
