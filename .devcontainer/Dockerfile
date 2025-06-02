# Imagem base CUDA oficial do PyTorch (ajuste a versão se quiser)
FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime

# Evita buffer
ENV PYTHONUNBUFFERED=1

# (Opcional) Set timezone, locale, etc.
ENV TZ=America/Sao_Paulo
RUN apt-get update && apt-get install -y tzdata git

WORKDIR /workspace

# Copie requirements.txt
COPY requirements.txt .

# Atualize pip, instale dependências
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Exponha as portas necessárias (ajuste conforme sua aplicação)
EXPOSE 8000 8888 6006
