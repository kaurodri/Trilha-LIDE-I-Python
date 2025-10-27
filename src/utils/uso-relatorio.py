from google import genai    #importar como google-genai
import os
from dotenv import load_dotenv
load_dotenv()
client = genai.Client(api_key = os.getenv("GOOGLE_API_KEY"))
prompt = "Olá gemini, me responda com 'ok'"
def transformar_relatorio(prompt):
    try:
        return client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
            thinking_config=genai.types.ThinkingConfig(thinking_budget=-1))  
        )
    except Exception as erro: 
        return f"erro do programa:{erro}"
resposta=transformar_relatorio(prompt)
print(f"resposta: {resposta.text}")