def extrair_acao(texto: str) -> dict:
    import json
    import re
    from actions import AIActions

    INTENTION_MAP = {
        "seguir jogador": AIActions.SEGUIR,
        "dar dinheiro": AIActions.DAR_DINHEIRO,
        "montar cavalo": AIActions.MONTAR_CAVALO,
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

            for campo in ["target", "say", "details"]:
                obj[campo] = obj.get(campo, "").strip()

            if len(obj["details"].split()) > 5:
                obj["details"] = "Muito detalhado"

            return {
                "type": INTENTION_MAP.get(intent_raw, AIActions.NENHUMA),
                "target": obj["target"] or None,
                "say": obj["say"] or None,
                "details": obj["details"] or "Sem detalhes."
            }

        except Exception:
            continue

    return {
        "type": AIActions.NENHUMA,
        "target": None,
        "say": None,
        "details": "Sem detalhes."
    }
