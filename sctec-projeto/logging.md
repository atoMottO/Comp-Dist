Padrão de Logging e Auditoria

O sistema implementa dois níveis de registo para garantir observabilidade e auditoria.

1. Logs de Aplicação (Técnicos)

Utilizados para depuração e rastreio do fluxo de execução. São visíveis na consola e no ficheiro app.log.

Formato: NÍVEL:TIMESTAMP:SERVIÇO:MENSAGEM

Exemplos:

INFO:2025-11-22T03:00:00Z:servico-agendamento:Requisição recebida para POST /agendamentos

INFO:2025-11-22T03:00:01Z:servico-agendamento:Tentando adquirir lock para recurso...

INFO:2025-11-22T03:00:02Z:servico-coordenador:Lock concedido.

2. Logs de Auditoria (Negócio)

Eventos críticos que alteram o estado do sistema (Criação ou Cancelamento) geram um registo estruturado em JSON (nível AUDIT). Estes logs são essenciais para resolver disputas entre cientistas.

Formato: Objeto JSON.

Exemplo (Criação):

{
  "timestamp_utc": "2025-11-22T03:00:05Z",
  "level": "AUDIT",
  "event_type": "AGENDAMENTO_CRIADO",
  "service": "servico-agendamento",
  "details": {
    "agendamento_id": 15,
    "cientista_id": 2,
    "horario_inicio_utc": "2025-12-01T04:00:00Z"
  }
}


Exemplo (Cancelamento):

{
  "timestamp_utc": "2025-11-22T03:05:00Z",
  "level": "AUDIT",
  "event_type": "AGENDAMENTO_CANCELADO",
  "service": "servico-agendamento",
  "details": { ...dados do agendamento... }
}
