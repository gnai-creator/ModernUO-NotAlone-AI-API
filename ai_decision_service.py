# ai_decision_service.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from ai_extract_action import extrair_acao
from prompt import montar_prompt_para_acao
from actions import AIActions
from memory import add_to_memory, get_memory
from models import FullNPCState, NPCDecision, NPCState
from text_generator import gerar_texto_com_tolerancia
import torch
import gc




MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

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
        result = gerar_texto_com_tolerancia(prompt, generator)
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

