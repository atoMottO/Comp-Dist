const express = require('express');
const app = express();
const port = 3000;

// O mapa 'locks' guarda o estado dos locks ativos
// Key: resource_id (ex: 'telescopio-1_2025-12-01T03:00:00Z')
// Value: O timestamp ou ID de quem possui o lock
const activeLocks = new Map();

// Middleware para logs simples no console
app.use((req, res, next) => {
    console.log(`INFO:${new Date().toISOString()}:servico-coordenador:Requisição recebida: ${req.method} ${req.originalUrl}`);
    next();
});

// Endpoint POST /lock/:resource_id
// Tenta adquirir um lock para o recurso especificado.
app.post('/lock/:resource_id', (req, res) => {
    const resourceId = req.params.resource_id;

    console.log(`Recebido pedido de lock para recurso ${resourceId}`); // Log do Porteiro 
    if (activeLocks.has(resourceId)) {
        // Recurso já travado: Permissão Negada
        console.log(`Recurso ${resourceId} já em uso, negando lock.`); // Log do Porteiro
        return res.status(409).json({ message: "Resource locked" }); // HTTP 409 Conflict 
    }

    // Recurso livre: Permissão Concedida
    activeLocks.set(resourceId, Date.now()); // Trava o recurso
    console.log(`Lock concedido para recurso ${resourceId}.`); // Log do Porteiro 
    return res.status(200).json({ message: "Lock acquired" }); // HTTP 200 OK 
});

// Endpoint POST /unlock/:resource_id
// Libera o lock para o recurso.
app.post('/unlock/:resource_id', (req, res) => {
    const resourceId = req.params.resource_id;
    
    console.log(`Recebido pedido de unlock para recurso ${resourceId}`); // Log do Porteiro

    if (activeLocks.delete(resourceId)) {
        console.log(`Lock para o recurso ${resourceId} liberado.`); // Log do Porteiro 
        return res.status(200).json({ message: "Lock released" });
    } else {
        // Tentar liberar um lock que não existe (pode ser um erro, mas retorna 200 para ser idempotente)
        return res.status(200).json({ message: "Resource was not locked or already released" });
    }
});

// Endpoint de status
app.get('/status', (req, res) => {
    const locksList = Array.from(activeLocks.keys());
    res.json({ status: "Coordenador Online", active_locks_count: locksList.length, active_locks: locksList });
});

app.listen(port, () => {
    console.log(`Serviço Coordenador (Porteiro) rodando na porta ${port}`);
});