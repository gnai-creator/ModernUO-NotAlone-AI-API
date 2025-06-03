FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime

# Ambiente
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo

# Diretório de trabalho
WORKDIR /workspace

# Copia arquivos de dependência
COPY requirements.txt .

# Instala sistema e Python deps
RUN apt-get update && \
    apt-get install -y tzdata git && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código para o container
COPY . .

# Expõe a porta da API
EXPOSE 10000

# Comando para iniciar o servidor
CMD ["uvicorn", "ai_service_instruct_phi:app", "--host", "0.0.0.0", "--port", "10000"]
