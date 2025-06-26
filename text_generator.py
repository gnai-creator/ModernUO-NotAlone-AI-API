import os
from openai import OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

def gerar_texto_com_tolerancia(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ou "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "Você é um NPC que responde em JSON conforme instruções."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=300,
        )

        return response.choices[0].message.content

    except Exception as e:
        print("[DEBUG] Erro na API do ChatGPT:", str(e))
        return '{"intention": "voltar à rotina", "target": "", "say": "Erro interno.", "money_amount": "0", "item_name": "", "details": ""}'
