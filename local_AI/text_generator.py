
def gerar_texto_com_tolerancia(prompt, tokenizer, model):
    try:
        prompt = prompt.encode("utf-8", "ignore").decode("utf-8")
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=8192)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        output = model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=True,
            top_k=50,
            top_p=0.9,
            temperature=0.8,
            pad_token_id=tokenizer.eos_token_id
        )

        if output is None or len(output) == 0:
            print("[DEBUG] Geração falhou: saída vazia.")
            return '{"intention": "voltar à rotina", "target": "", "say": "Estou confuso...", "money_amount": "0", "item_name": "", "details": ""}'

        # DECODIFICAÇÃO CORRETA:
        decoded = tokenizer.decode(output[0], skip_special_tokens=True)
        return decoded

    except Exception as e:
        print("[DEBUG] Erro inesperado na geração:", str(e))
        return '{"intention": "voltar à rotina", "target": "", "say": "Erro interno.", "money_amount": "0", "item_name": "", "details": ""}'
