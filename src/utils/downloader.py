import yt_dlp
import os
import tempfile
import streamlit as st

def baixar_audio_ytdlp(link):
    """
    Baixa apenas o áudio do vídeo fornecido, de forma robusta.
    Usa cookies e user-agent para contornar bloqueios de região/idade.
    """
    try:
        temp_dir = tempfile.mkdtemp()
        out_path = os.path.join(temp_dir, "audio.%(ext)s")

        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': out_path,
            'quiet': True,
            'no_warnings': True,
            'cookiefile': 'cookies.txt',  # opcional, exportar cookies do navegador
            'user-agent': 'Mozilla/5.0',   # evita bloqueios básicos
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            audio_file = ydl.prepare_filename(info)
            return audio_file

    except Exception as e:
        st.error(f"Erro ao baixar áudio: {e}")
        return None
