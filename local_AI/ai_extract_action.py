
def extrair_acao(texto: str) -> dict:
    import json
    import re
    from actions import AIActions
    from maps import INTENTION_MAP, ITEM_MAP


    
    print(f"[DEBUG] Extraindo ação: {texto}")
    # Limpeza de lixo
    texto = texto.replace("```json", "")
    texto = texto.replace("```", "")
    texto = re.sub(r"```.*?```", "", texto, flags=re.DOTALL)
    texto = re.sub(r"[`#].*", "", texto)
    texto = texto.strip()

    blocos = re.finditer(r"{[^{}]*\"intention\"[^{}]*}", texto, re.DOTALL)
    decoder = json.JSONDecoder()

    for idx, match in enumerate(blocos):
        try:
            obj_raw = texto[match.start():match.end()]
            
            # Substitua o bloco que manipula o JSON extraído por:
            obj, _ = decoder.raw_decode(obj_raw)

            if not isinstance(obj, dict):
                continue

            # Normaliza todos os campos para string
            def safe_str(value):
                if value is None:
                    return ""
                if isinstance(value, (int, float)):
                    return str(value)
                return str(value).strip()

            intent_raw = safe_str(obj.get("intention")).lower()
            if not intent_raw:
                continue

            return {
                "type": INTENTION_MAP.get(intent_raw, AIActions.NENHUMA),
                "target": safe_str(obj.get("target")) or None,
                "say": safe_str(obj.get("say")) or None,
                "money_amount": safe_str(obj.get("money_amount")),
                "item_name": ITEM_MAP.get(safe_str(obj.get("item_name")), None) if obj.get("item_name") in ITEM_MAP else "",
                "details": " ".join(safe_str(obj.get("details")).split()[:5]) or "Sem detalhes."
            }


        except Exception as e:
            print(f"[DEBUG] Erro ao extrair ação: {str(e)} — Conteúdo: {texto}")

    # Fallback se nada foi extraído com sucesso
    return {
        "type": AIActions.NENHUMA,
        "target": None,
        "say": None,
        "money_amount": "0",
        "item_name": None,
        "details": "Sem detalhes."
    }
