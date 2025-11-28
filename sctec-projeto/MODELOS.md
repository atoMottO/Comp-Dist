Modelos de Entidades (SCTEC)

1. Agendamento

Representa a reserva de um slot de tempo no telescópio. É a entidade central para garantir a exclusão mútua, pois não podem existir dois agendamentos com o mesmo horario_inicio_utc.

Campo

Tipo

Descrição

id

Integer

Identificador único (Chave Primária).

cientista_id

Integer

ID do cientista que solicitou a reserva.

horario_inicio_utc

String (ISO 8601)

Data e hora do início da observação (ex: "2025-12-01T03:00:00Z"). Deve ser único.

2. Cientista

Entidade lógica representada pelo ID enviado na requisição. No protótipo atual, não existe uma tabela dedicada, sendo o cientista identificado apenas pelo seu ID numérico.

Campo

Tipo

Descrição

id

Integer

Identificador único do cientista.