from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from transformers import pipeline
from src.ai_extract_action import extrair_acao
from ai_action_prompt import montar_prompt_para_acao

app = FastAPI()

# Use o seu pipeline existente:
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

class NearbyNPC(BaseModel):
    id: str
    name: str
    role: str
    mood: Optional[str] = "neutro"

class NPCState(BaseModel):
    npc_id: str
    name: str
    role: str
    location: str
    mood: Optional[str] = "neutro"
    memory: Optional[List[str]] = []
    nearby_npcs: Optional[List[NearbyNPC]] = []

@app.post("/npc/next_action")
def next_action(npc: NPCState):
    prompt = montar_prompt_para_acao(npc)
    
    result = generator(prompt, max_new_tokens=40, do_sample=True, temperature=0.7)[0]['generated_text']

    # Extração simples dos campos (pode ser melhorado com regex/json)
    parsed = extrair_acao(result)

    return parsed





