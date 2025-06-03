from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import os

MODEL_NAME = "microsoft/phi-2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,  # CPU compatível
    device_map="auto"           # vai cair para CPU automaticamente
)

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)

app = FastAPI()

class NPCRequest(BaseModel):
    npc: str
    role: str
    background: str
    input: str
    player: str

def montar_prompt(npc, role, background, input_text, history_list=None):
    prompt = f"""Você está interpretando {npc}, um {role}.
Personalidade: {background}.
Este é um mundo fictício chamado Ultima Online.
Não mencione sistemas de IA. Fale como o personagem.
"""
    if history_list:
        for who, msg in history_list:
            prefix = "Jogador:" if who == "player" else f"{npc}:"
            prompt += f"{prefix} {msg}\n"
    prompt += f"Jogador: {input_text}\n{npc}:"
    return prompt.strip()

# Memória RAM simples por jogador
memory_store = {}
MEMORY_WINDOW = 10

def add_to_memory(npc, player, role, text):
    key = (npc, player)
    if key not in memory_store:
        memory_store[key] = []
    memory_store[key].append((role, text))
    if len(memory_store[key]) > 50:
        memory_store[key] = memory_store[key][-50:]

def get_memory(npc, player):
    return memory_store.get((npc, player), [])[-MEMORY_WINDOW:]

@app.post("/think")
async def think(req: NPCRequest):
    history = get_memory(req.npc, req.player)
    prompt = montar_prompt(req.npc, req.role, req.background, req.input, history)

    output = generator(
        prompt,
        max_new_tokens=40,
        do_sample=True,
        temperature=0.9,
        top_p=0.92,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )[0]['generated_text']

    resposta = output[len(prompt):].strip()
    palavras = resposta.split()
    if len(palavras) > 16:
        resposta = ' '.join(palavras[:16]) + "..."
    resposta = ' '.join(resposta.replace('\n', ' ').replace('\r', ' ').split())

    add_to_memory(req.npc, req.player, "player", req.input)
    add_to_memory(req.npc, req.player, "npc", resposta)

    return {"action": "Say", "text": resposta}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
