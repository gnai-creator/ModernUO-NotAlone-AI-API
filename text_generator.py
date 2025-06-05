from transformers import pipeline
import torch

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
def gerar_texto_com_tolerancia(prompt, generator):
    try:
        return generator(
            prompt,
            max_new_tokens=120,
            do_sample=True,
            temperature=1.0,
            top_k=50,
            top_p=0.95
        )[0]['generated_text']
    except Exception as e:
        print("[DEBUG] Geração falhou, não será reprocessada:", e)
        raise e  # Deixa o FastAPI capturar o erro e retornar via fallback do endpoint
