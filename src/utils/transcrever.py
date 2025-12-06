import whisper
import os
import time


def transcrever_audio(arquivo):
    """Carrega o modelo Whisper e transcreve o arquivo fornecido.

    Retorna o dicionário de resultado do modelo em caso de sucesso,
    ou um dicionário com a chave 'erro' em caso de exceção.
    """
    try:
        carregar_modelo = whisper.load_model("base", fp16=False)
        transcrever = carregar_modelo.transcribe(arquivo)
        return transcrever
    except Exception as e:
        return {"erro": str(e)}
    finally:
        try:
            if arquivo and os.path.exists(arquivo):
                os.remove(arquivo)
        except Exception:
            pass


# Diretório base do projeto (dois níveis acima deste arquivo)
BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_AUDIO_DIR = os.path.join(BASE_DIR, "src", "temp")


def validar_arquivo(audio_filename="audio.opus", timeout=60, poll_interval=5):
    """Espera até o arquivo aparecer em `DEFAULT_AUDIO_DIR`.

    Retorna o caminho absoluto do arquivo quando encontrado, ou `None` se o timeout expirar.
    """
    caminho_arquivo = os.path.join(DEFAULT_AUDIO_DIR, audio_filename)
    caminho_arquivo = os.path.normpath(caminho_arquivo)

    start = time.time()
    while not os.path.isfile(caminho_arquivo):
        if timeout is not None and (time.time() - start) > timeout:
            return None
        time.sleep(poll_interval)

    return caminho_arquivo


def rodar_scripti(timeout=60):
    """Valida a existência do arquivo de áudio e executa a transcrição.

    Retorna o texto transcrito (str) em caso de sucesso, ou `None` em caso de erro/timeout.
    """
    caminho = validar_arquivo(timeout=timeout)
    if not caminho:
        return None

    resultado = transcrever_audio(caminho)
    if isinstance(resultado, dict) and "erro" in resultado:
        return None

    # Resultado esperado: dicionário com chave 'text'
    if isinstance(resultado, dict):
        return resultado.get("text")
    return None
