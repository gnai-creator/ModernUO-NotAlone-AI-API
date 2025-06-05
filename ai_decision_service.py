# ai_decision_service.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from ai_extract_action import extrair_acao
from prompt import montar_prompt, montar_prompt_para_acao
from actions import AIActions
from memory import add_to_memory, get_memory
from models import FullNPCState, NPCDecision, NPCState
import torch
import gc




MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

app = FastAPI()


# Apaga o modelo e pipeline atuais (se existirem)
try:
    del model
    del generator
except:
    pass

# Libera memória da GPU
gc.collect()
torch.cuda.empty_cache()

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)


@app.post("/npc/decide")
def npc_decide(state: FullNPCState):
    try:
        # === Caso 2: IA decide ação autônoma ===
        prompt = montar_prompt_para_acao(state)
        result = generator(prompt, max_new_tokens=100, do_sample=True, temperature=0.7)[0]['generated_text']
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
        return {
            "type": AIActions.NENHUMA,
            "target": None,
            "say": None,
            "money_amount": "0",
            "item": None,
            "details": "Erro ao decidir ação: " + str(e)
        }

