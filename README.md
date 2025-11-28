# Relatório do Projeto – Comp-Dist

## Decisões de projeto
O projeto foi desenvolvido com uma arquitetura distribuída baseada em microserviços independentes. As principais decisões foram:

- **Serviço Coordenador (Node.js):** responsável por orquestrar o fluxo do sistema e servir como gateway.
- **Serviço de Agendamento (Python/Flask):** responsável pela lógica de processamento e simulação das ações.
- Comunicação entre serviços realizada pela **rede interna do Docker**, utilizando nomes de container como hosts.
- Uso de **Docker Compose** para gerenciar, subir e padronizar o ambiente.

---

## O que conseguimos implementar
- Estrutura completa em dois microserviços funcionais.
- Comunicação estável entre os serviços via Docker.
- Rotas operacionais em ambos os serviços (Node e Flask).
- Execução concorrente via script Python (`test_concurrency.py`).
- Ambiente reproduzível usando `docker compose up --build`.
- Parametrização da URL do coordenador via variável de ambiente (`COORDINATOR_URL`).

---

## Dificuldades encontradas
- Erros ao tentar construir imagens Docker devido a caminhos incorretos dos Dockerfiles.
- Cliente Python não conseguia acessar containers pelo nome (precisando usar `localhost`).
- Falta de documentação clara das rotas, exigindo leitura direta do código.
- Necessidade de testar a network do Docker para confirmar a comunicação entre serviços.

---

## O que não conseguimos implementar
- Persistência de dados em banco de dados.
- Autenticação, autorização e segurança avançada.
- Documentação automática da API (Swagger).
- Persistência real dos "cientistas" criados.

---

## O que pode ser melhorado
- Integrar banco de dados.
- Adicionar flags para comunicação assíncrona.
- Padronizar respostas das APIs e status HTTP.

---

## É possível criar cientistas?
- O sistema permite criar instâncias temporárias de cientistas a partir das requisições recebidas.  
- MAS ele não cria cientistas persistentes, nem gera cientistas automaticamente.  
- Os dados não são armazenados pois tudo é perdido ao encerrar os containers.
