# ai_decision_service.py
from fastapi import FastAPI
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from ai_extract_action import extrair_acao
from prompt import montar_prompt_para_acao
from actions import AIActions
from models import FullNPCState
from text_generator import gerar_texto_com_tolerancia
import torch




MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    pad_token_id=tokenizer.eos_token_id
)

app = FastAPI()



@app.post("/npc/decide")
def npc_decide(state: FullNPCState):
    try:
        # === Caso 2: IA decide ação autônoma ===
        prompt = montar_prompt_para_acao(state)
        
        # tokens = tokenizer(prompt, return_tensors="pt").input_ids
        # print(f"[DEBUG] Tamanho do prompt: {tokens.shape[-1]} tokens.")
        # print(f"[DEBUG] Tokens de entrada: {tokens[0].tolist()}")

        result = gerar_texto_com_tolerancia(prompt, tokenizer, model)
        if not result or not isinstance(result, str):
            raise ValueError("Resultado da geração está vazio ou inválido.")

        print("[DEBUG] Resultado gerado:", result)
        parsed = extrair_acao(result)
        print("[DEBUG] Ação extraída:", parsed["type"])
        return {
            "type": parsed.get("type", AIActions.NENHUMA),
            "target": parsed.get("target"),
            "say": parsed.get("say"),
            "money_amount": parsed.get("money_amount"),
            "item": parsed.get("item"),
            "details": parsed.get("details")
        }
    except Exception as e:
        print("[DEBUG] Erro ao decidir ação:", e)
        if "device meta" in str(e):
            print("[DEBUG] Pipeline possivelmente corrompido — reinício pode ser necessário futuramente.")
        return {
            "type": AIActions.NENHUMA,
            "target": None,
            "say": None,
            "money_amount": "0",
            "item": None,
            "details": "Erro ao decidir ação: " + str(e)
        }

