from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

MODEL_NAME = "Qwen/Qwen3-1.7B"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1
)

app = FastAPI()

memory_store = {}
MEMORY_WINDOW = 10

class NPCRequest(BaseModel):
    npc: str
    role: str
    background: str
    input: str
    player: str

def montar_prompt(npc, role, background, input_text, history_list=None):
    prompt = f"{npc} é um {role}. Personalidade: {background}.\n"
    if history_list:
        for who, msg in history_list:
            prefix = "Jogador" if who == "player" else npc
            prompt += f"{prefix}: {msg}\n"
    prompt += f"Jogador: {input_text}\n{npc}:"
    return prompt

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

@app.post("/think")
async def think(req: NPCRequest):
    history_list = get_memory(req.npc, req.player)
    prompt = montar_prompt(req.npc, req.role, req.background, req.input, history_list)
    output = generator(
        prompt,
        max_new_tokens=128,
        do_sample=True,
        temperature=0.9,
        top_p=0.92,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id
    )[0]['generated_text']
    resposta = output[len(prompt):].strip()
    # Limpa caso venha prefixo repetido
    if resposta.startswith(f"{req.npc}:"):
        resposta = resposta[len(f"{req.npc}:"):].strip()
    add_to_memory(req.npc, req.player, "player", req.input)
    add_to_memory(req.npc, req.player, "npc", resposta)
    return {"action": "Say", "text": resposta}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
