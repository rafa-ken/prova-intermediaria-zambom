# Etapa de execução
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o projeto
COPY . .

# Expor a porta do Flask
EXPOSE 5000

# Rodar o Flask com Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]