import os
import yaml
import yt_dlp
TEMP_ENDERECO = './src/temp'
SETTINGS_ENDERECO = './src/config/settings.yaml'
def midia_audio(link):
    if not os.path.exists(TEMP_ENDERECO):
        os.makedirs(TEMP_ENDERECO)

    with open(SETTINGS_ENDERECO) as f:
        youtube_config = yaml.safe_load(f)

    with yt_dlp.YoutubeDL(youtube_config) as youtube:
        youtube.download([link])
    return True

resposta = midia_audio("https://www.youtube.com/shorts/XyV7f48qoZ0")
resposta