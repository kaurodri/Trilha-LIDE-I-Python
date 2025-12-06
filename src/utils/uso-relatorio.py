from google import genai    # importar como google-genai
import os
from dotenv import load_dotenv
import sys
load_dotenv()

# Import resiliente: tenta import pelo package (quando executado com -m) e faz fallback
try:
    from src.utils.transcrever import rodar_scripti
except Exception:
    # Se o script for executado diretamente (python src\utils\uso-relatorio.py),
    # o diretório do script aparece em sys.path, então podemos importar o módulo irmão.
    script_dir = os.path.dirname(__file__)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    from transcrever import rodar_scripti

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def transformar_relatorio(prompt: str):
    try:
        return client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                thinking_config=genai.types.ThinkingConfig(thinking_budget=-1)
            ),
        )
    except Exception as erro:
        return f"erro do programa:{erro}"


def gerar_relatorio(timeout: int = 60):
    """Orquestra a transcrição e a geração do relatório.

    - Espera pela transcrição via `rodar_scripti` (com timeout)
    - Lê o modelo de relatório em `relatorio/README.md` (caminho relativo ao arquivo)
    - Chama a API de geração e imprime o resultado
    """
    texto_transcrito = rodar_scripti(timeout=timeout)
    if not texto_transcrito:
        print("Nenhum áudio transcrito (timeout ou erro).")
        return

    base_dir = os.path.dirname(__file__)
    rel_path = os.path.join(base_dir, "relatorio", "README.md")
    try:
        with open(rel_path, "r", encoding="utf-8") as arquivo:
            relatorio_modelo = arquivo.read()
    except Exception as e:
        print(f"Não foi possível ler o modelo de relatório: {e}")
        relatorio_modelo = ""

    prompt = f"utilize o seguinte texto ```{texto_transcrito}``` para gerar um relatorio com os seguinte modelo:{relatorio_modelo}"
    resposta = transformar_relatorio(prompt)
    if isinstance(resposta, str):
        print(f"resposta: {resposta}")
    else:
        # A API pode retornar objetos com diferentes atributos; tente acessar `.text` ou `.output`.
        text = getattr(resposta, "text", None) or getattr(resposta, "output", None) or str(resposta)
        print(f"resposta: {text}")


if __name__ == "__main__":
    gerar_relatorio()