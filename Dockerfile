FROM python:3.12-slim

WORKDIR /app

# Copiar requirements primeiro para cache de dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo da aplicacao
COPY . .

# Variavel de ambiente para Python
ENV PYTHONUNBUFFERED=1

# Expor porta padrao da API
EXPOSE 8000

# Comando padrao (API)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
