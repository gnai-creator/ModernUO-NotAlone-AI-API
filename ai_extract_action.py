def extrair_acao(texto: str) -> dict:
    import json
    import re
    from actions import AIActions

    INTENTION_MAP = {
        # "seguir jogador": AIActions.SEGUIR,
        # "montar cavalo": AIActions.MONTAR_CAVALO,
        "receber dinheiro": AIActions.PEGAR_DINHEIRO,
        "pegar dinheiro": AIActions.PEGAR_DINHEIRO,
        "dar dinheiro": AIActions.DAR_DINHEIRO,
        "dar item": AIActions.DAR_ITEM,
        "atacar": AIActions.ATACAR,
        "voltar à rotina": AIActions.ROTINA,
        "voltar a rotina": AIActions.ROTINA,
        "idle": AIActions.NENHUMA,
        "nenhuma ação": AIActions.NENHUMA,
        "": AIActions.NENHUMA
    }

    # Limpeza de markdown e comentários
    texto = re.sub(r"```.*?```", "", texto, flags=re.DOTALL)
    texto = re.sub(r"```", "", texto)
    texto = re.sub(r"//.*", "", texto)
    texto = re.sub(r"#.*", "", texto)
    texto = texto.strip()

    # Procura todos os JSONs com "intention"
    blocos = re.finditer(r"{[^{}]*\"intention\"[^{}]*}", texto, re.DOTALL)
    decoder = json.JSONDecoder()

    for match in blocos:
        try:
            obj, _ = decoder.raw_decode(texto[match.start():])
            if not isinstance(obj, dict):
                continue

            # Ignora blocos vazios
            intent_raw = obj.get("intention", "").strip().lower()
            if intent_raw == "":
                continue

            for campo in ["target", "say", "money_amount", "details"]:
                obj[campo] = obj.get(campo, "").strip()

            if len(obj["details"].split()) > 5:
                obj["details"] = "Muito detalhado"

            return {
                "type": INTENTION_MAP.get(intent_raw, AIActions.NENHUMA),
                "target": obj["target"] or None,
                "say": obj["say"] or None,
                "money_amount": obj["money_amount"] or "0",
                "details": obj["details"] or "Sem detalhes."
            }

        except Exception:
            print(f"Erro ao extrair ação: {texto}")
            return {
                "type": AIActions.NENHUMA,
                "target": None,
                "say": None,
                "money_amount": "0",
                "details": "Sem detalhes."
            }
