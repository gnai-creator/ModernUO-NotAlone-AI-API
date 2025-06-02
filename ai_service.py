from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

app = FastAPI()

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Chat"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, trust_remote_code=True,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1
)

# -------- Memória longa --------
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
    key = (npc, player)
    if key in memory_store:
        return memory_store[key][-MEMORY_WINDOW:]
    return []

class NPCRequest(BaseModel):
    npc: str
    role: str
    background: str
    input: str
    player: str  # Quem está conversando com o NPC

@app.post("/think")
async def think(req: NPCRequest):
    # Resgata histórico
    history_list = get_memory(req.npc, req.player)
    # Monta prompt
    prompt = f"SYSTEM: Você é {req.npc}, um {req.role}. Personalidade: {req.background}.\n"
    for who, msg in history_list:
        prefix = "USER" if who == "player" else "ASSISTANT"
        prompt += f"{prefix}: {msg}\n"
    prompt += f"USER: {req.input}\nASSISTANT:"

    # Gera resposta
    output = generator(
        prompt,
        max_length=128,
        do_sample=True,
        temperature=0.9,
        top_p=0.92,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id
    )[0]['generated_text']
    resposta = output[len(prompt):].strip()
    if resposta.startswith("ASSISTANT:"):
        resposta = resposta[len("ASSISTANT:"):].strip()
    if resposta.startswith(f"{req.npc}:"):
        resposta = resposta[len(f"{req.npc}:"):].strip()
    
    # Salva no histórico (pergunta do player + resposta do NPC)
    add_to_memory(req.npc, req.player, "player", req.input)
    add_to_memory(req.npc, req.player, "npc", resposta)

    return {"action": "Say", "text": resposta}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
