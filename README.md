# ModernUO NotAlone AI API

## Visão Geral

O **ModernUO NotAlone AI API** é um microserviço inteligente para servidores Ultima Online, integrando IA conversacional avançada com memória longa para NPCs (personagens não-jogadores) usando modelos LLM de última geração, como Qwen2.5-1.5B-Chat.

Cada NPC responde de forma única, com personalidade, histórico próprio e memória individualizada para cada jogador, proporcionando interações profundas e realistas.

---

## Como Funciona a Dinâmica

### 1. Estrutura Geral

* O serviço roda como uma API REST (FastAPI) acessível por `/think`.
* Utiliza o modelo Qwen2.5-1.5B-Chat para geração de texto e roleplay.
* Mantém histórico individualizado de conversas (memória longa) para cada par NPC-jogador.

### 2. Fluxo de interação

1. **O jogador envia uma mensagem a um NPC**
2. O microserviço:

   * Recupera o histórico recente da conversa entre o NPC e aquele jogador.
   * Monta um prompt detalhado, incluindo:

     * Nome do NPC
     * Papel/role do NPC
     * Background/persona
     * Histórico das últimas interações
     * A mensagem atual do jogador
   * Envia esse contexto para o modelo LLM (Qwen2.5)
3. **O LLM gera uma resposta personalizada** baseada na personalidade do NPC, memória da conversa e contexto atual.
4. O microserviço retorna a resposta pronta para ser exibida no servidor ModernUO.
5. O histórico da conversa é atualizado, permitindo continuidade e memória viva.

### 3. Exemplo de prompt interno

```
SYSTEM: Você é Oberon, um mago. Personalidade: Oberon é misterioso, fala em enigmas, detesta guerreiros barulhentos.
USER: Como aprendo magia?
ASSISTANT: Apenas quem escuta o silêncio dos astros pode receber tal dom...
USER: Você já enfrentou dragões?
ASSISTANT: Muitas lendas contam, mas poucos sobreviveram para dizer...
USER: Pode me ensinar?
ASSISTANT:
```

A resposta gerada será sempre consistente com a memória e personalidade do NPC.

### 4. Como é a "memória longa"

* A memória longa é um histórico das últimas interações (perguntas do jogador e respostas do NPC).
* Para cada par (NPC, jogador), o serviço mantém essa memória em RAM (pode ser expandido para arquivo ou banco de dados).
* O tamanho da janela de memória é configurável (ex: 10 últimas falas).
* Se a conversa for muito longa, só as últimas interações entram no prompt, mas toda a história pode ser persistida/recuperada.

---

## Uso da API `/think`

### Payload JSON

```json
{
  "npc": "Oberon",
  "role": "mago",
  "background": "Oberon é misterioso, fala em enigmas, detesta guerreiros barulhentos.",
  "input": "Como aprendo magia?",
  "player": "Felipe" // identificação única do jogador
}
```

### Resposta JSON

```json
{
  "action": "Say",
  "text": "Apenas quem escuta o silêncio dos astros pode receber tal dom..."
}
```

---

## Como Integrar

1. Faça requisições HTTP POST para o endpoint `/think`, enviando o payload JSON.
2. Receba a resposta com a fala pronta do NPC, pronta para exibição no mundo ModernUO.
3. Repita: o serviço lembrará do histórico de cada jogador/NPC!

---

## Como rodar

* Com Python e dependências instaladas:

```bash
uvicorn translator_service:app --host 0.0.0.0 --port 8000
```

* Ou via Docker/DevContainer (ver instruções do projeto).

---

## Pontos fortes

* **NPCs únicos:** Cada personagem pode ter seu próprio nome, papel e personalidade.
* **Memória longa real:** NPCs lembram das conversas, mudam com o tempo, reconhecem jogadores.
* **LLM poderoso:** Suporte a múltiplos idiomas e roleplay natural.
* **Fácil de integrar** com ModernUO e outros sistemas.

---

## Extensões possíveis

* Persistência de memória em banco de dados
* Logs para debugging de IA
* Tradução automática via microserviço dedicado
* Compartilhamento de memória global entre NPCs (lore do mundo)
* Personalidade e evolução adaptativa

---

**Projeto ideal para criar servidores Ultima Online realmente vivos e inteligentes!**
