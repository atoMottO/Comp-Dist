# Usa uma imagem oficial leve do Python
FROM python:3.9-slim

# Define a pasta de trabalho dentro do contentor
WORKDIR /app

# Copia o ficheiro de dependências primeiro (para aproveitar o cache do Docker)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do código para dentro do contentor
COPY . .

# Expõe a porta 5000 (onde o Flask corre)
EXPOSE 5000

# Define a variável de ambiente para o Flask correr em modo visível externamente
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para iniciar a aplicação
CMD ["flask", "run"]