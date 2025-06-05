import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def gerar_texto_com_tolerancia(prompt, tokenizer, model):
    try:
        prompt = prompt.encode("utf-8", "ignore").decode("utf-8")  # segurança extra
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=8192)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        output = model.generate(
            **inputs,
            max_new_tokens=110,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

        if output is None or len(output) == 0:
            raise ValueError("Geração vazia.")

        return tokenizer.decode(output[0], skip_special_tokens=True)

    except Exception as e:
        print("[DEBUG] Geração falhou:", str(e))
        raise e

