import whisper
from pydub import AudioSegment
import streamlit as st

model = whisper.load_model("base")  # Pode usar small, medium ou large

def dividir_audio(caminho_audio, duracao_segundos=600):
    chunks = []
    audio = AudioSegment.from_file(caminho_audio)
    for i in range(0, len(audio), duracao_segundos*1000):
        chunk_path = f"{caminho_audio}_chunk{i//1000}.mp3"
        audio[i:i+duracao_segundos*1000].export(chunk_path, format="mp3")
        chunks.append(chunk_path)
    return chunks

def transcrever_audio(caminho_audio):
    """
    Transcreve áudio em chunks para suportar vídeos longos.
    """
    try:
        st.info("🎙️ Dividindo áudio em partes...")
        chunks = dividir_audio(caminho_audio)
        st.info(f"✅ Áudio dividido em {len(chunks)} partes.")

        transcricao_completa = ""
        for idx, chunk in enumerate(chunks):
            st.info(f"⏳ Transcrevendo parte {idx+1} de {len(chunks)}...")
            result = model.transcribe(chunk, fp16=False)
            transcricao_completa += result["text"] + "\n"

        return transcricao_completa

    except Exception as e:
        st.error(f"Erro na transcrição: {e}")
        return ""
