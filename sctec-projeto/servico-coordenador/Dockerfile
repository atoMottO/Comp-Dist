# Usa uma imagem oficial leve do Node.js
FROM node:18-alpine

# Define a pasta de trabalho
WORKDIR /app

# Copia os ficheiros de definição do projeto
COPY package*.json ./

# Instala as dependências
RUN npm install

# Copia o código da aplicação
COPY . .

# Expõe a porta 3000 (onde o Express corre)
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["node", "server.js"]