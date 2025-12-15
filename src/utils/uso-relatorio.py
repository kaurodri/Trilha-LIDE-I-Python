import openai
import os
import streamlit as st
from dotenv import load_dotenv

# Carregar API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_relatorio_gpt(transcricao_do_video):
    try:
        prompt = f"""
Você é uma inteligência artificial especialista em análise de conteúdo de vídeos.

Abaixo será fornecida a transcrição completa de um vídeo extraído da internet (como YouTube). Sua tarefa é gerar um *RELATÓRIO COMPLETO E BEM ORGANIZADO*, com base apenas no conteúdo transcrito.

⚠ IMPORTANTE:
- A transcrição pode conter erros de pontuação ou trechos mal formatados. Interprete com cuidado.
- Não cite diretamente trechos com erros, prefira reescrever ou resumir.
- NÃO repita a transcrição. O objetivo é produzir um texto novo, claro e objetivo, a partir dela.

🎯 O RELATÓRIO DEVE SEGUIR A ESTRUTURA ABAIXO:

---

📄 *RELATÓRIO DE ANÁLISE DE VÍDEO*

1. *Título sugerido para o relatório:*
2. *Introdução:*
3. *Sumário:*
4. *Desenvolvimento:*
   a. *Resumo do conteúdo:* 
   b. *Principais tópicos:* 
   c. *Objetivo do vídeo:* 
   d. *Público-alvo:* 
   e. *Tom e estilo:*
5. *Conclusão:*
6. *Observações Finais (caso existam):*

---

Abaixo está a transcrição do vídeo:

\"\"\"{transcricao_do_video}\"\"\"
"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente que gera relatórios resumidos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.5,
        )
        resumo = response.choices[0].message.content.strip()
        return resumo
    except Exception as e:
        st.error(f"Erro ao gerar relatório: {e}")
        return "Não foi possível gerar o relatório."
