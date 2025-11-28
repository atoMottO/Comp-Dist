Especificação da API RESTful

Este documento descreve os endpoints disponíveis nos dois microsserviços do sistema SCTEC.

Serviço de Agendamento (Cérebro)

Porta: 5000 (ou http://localhost:5000 via Docker)

1. Sincronização de Tempo

Método: GET

Rota: /time

Descrição: Retorna a hora oficial do servidor para sincronização de relógios (Algoritmo de Cristian).

Resposta (200 OK):

{ "server_time": "2025-12-01T12:00:00Z" }


2. Criar Agendamento

Método: POST

Rota: /agendamentos

Descrição: Tenta reservar um horário. O serviço comunica com o Coordenador para obter um lock antes de gravar.

Corpo (JSON):

{ "cientista_id": 1, "horario_inicio_utc": "2025-12-01T03:00:00Z" }


Respostas:

201 Created: Agendamento criado com sucesso.

409 Conflict: Horário ocupado (falha no Lock ou registo duplicado).

3. Listar Agendamentos

Método: GET

Rota: /agendamentos

Descrição: Lista todos os agendamentos ativos com links HATEOAS.

Resposta (200 OK): Lista JSON de objetos agendamento.

4. Cancelar Agendamento

Método: DELETE

Rota: /agendamentos/<id>/cancel

Descrição: Remove um agendamento e gera um log de auditoria.

Resposta: 200 OK se cancelado com sucesso.

Serviço Coordenador (Porteiro)

Porta: 3000 (Comunicação interna via rede Docker)

1. Adquirir Lock

Método: POST

Rota: /lock/:resource_id

Descrição: Tenta travar um recurso específico (ex: data/hora).

Respostas:

200 OK: Lock adquirido (permitido).

409 Conflict: Lock negado (já em uso).

2. Libertar Lock

Método: POST

Rota: /unlock/:resource_id

Descrição: Liberta o recurso para outros utilizadores.

Resposta: 200 OK.