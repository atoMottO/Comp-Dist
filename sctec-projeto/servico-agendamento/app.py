import os
import requests
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# --- Configuração ---
COORDINATOR_URL = os.environ.get('COORDINATOR_URL', 'http://localhost:3000')

# --- Configuração de Logging ---
LOG_FILE = 'app.log'
AUDIT_LOG_LEVEL = 25 
logging.addLevelName(AUDIT_LOG_LEVEL, "AUDIT")

def setup_logging():
    logger = logging.getLogger('sctec_scheduler')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(levelname)s:%(asctime)s:servico-agendamento:%(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S.000Z'
    )

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    def audit(self, message, *args, **kws):
        if self.isEnabledFor(AUDIT_LOG_LEVEL):
            self._log(AUDIT_LOG_LEVEL, message, args, **kws)
    
    logging.Logger.audit = audit
    return logger

logger = setup_logging()

# --- Configuração do Flask e Banco de Dados ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agendamento.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Agendamento
class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cientista_id = db.Column(db.Integer, nullable=False)
    horario_inicio_utc = db.Column(db.String, unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'cientista_id': self.cientista_id,
            'horario_inicio_utc': self.horario_inicio_utc
        }

with app.app_context():
    db.create_all()

# --- Funções de Lock ---
def acquire_lock(resource_id):
    url = f"{COORDINATOR_URL}/lock/{resource_id}"
    logger.info(f"Tentando adquirir lock para o recurso {resource_id}")
    try:
        response = requests.post(url, timeout=5)
        if response.status_code == 200:
            logger.info(f"Lock adquirido com sucesso para o recurso {resource_id}")
            return True
        elif response.status_code == 409:
            logger.info(f"Falha ao adquirir lock, recurso ocupado: {resource_id}")
            return False
        else:
            logger.error(f"Erro inesperado ao tentar adquirir lock: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de comunicação com o Serviço Coordenador: {e}")
        return False

def release_lock(resource_id):
    url = f"{COORDINATOR_URL}/unlock/{resource_id}"
    logger.info(f"Liberando lock para o recurso {resource_id}")
    try:
        requests.post(url, timeout=5)
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao tentar liberar lock: {e}")

# --- Endpoints ---
@app.route('/agendamentos', methods=['POST'])
def create_agendamento():
    data = request.get_json()
    horario_inicio_utc = data.get('horario_inicio_utc')
    cientista_id = data.get('cientista_id')
    
    logger.info(f"Requisição recebida para POST /agendamentos para o recurso {horario_inicio_utc}")
    
    if not horario_inicio_utc or not cientista_id:
        return jsonify({"message": "Dados inválidos."}), 400

    resource_id = f"telescopio-1_{horario_inicio_utc}"
    lock_acquired = False
    
    try:
        lock_acquired = acquire_lock(resource_id)

        if not lock_acquired:
            return jsonify({"message": "Slot de horário em uso. Tente novamente."}), 409

        logger.info("Iniciando verificação de conflito no BD")
        
        existing_agendamento = Agendamento.query.filter_by(horario_inicio_utc=horario_inicio_utc).first()
        if existing_agendamento:
            return jsonify({"message": "Horário já agendado."}), 409

        novo_agendamento = Agendamento(cientista_id=cientista_id, horario_inicio_utc=horario_inicio_utc)
        db.session.add(novo_agendamento)
        db.session.commit()
        logger.info("Salvando novo agendamento no BD")

        audit_log = {
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "level": "AUDIT",
            "event_type": "AGENDAMENTO_CRIADO",
            "service": "servico-agendamento",
            "details": novo_agendamento.to_dict()
        }
        logger.audit(json.dumps(audit_log))

        response_data = novo_agendamento.to_dict()
        response_data['_links'] = {
            'self': {'href': f"/agendamentos/{novo_agendamento.id}"},
            'cancel': {'href': f"/agendamentos/{novo_agendamento.id}/cancel", 'method': 'DELETE'}
        }
        return jsonify(response_data), 201

    finally:
        if lock_acquired:
            release_lock(resource_id)

@app.route('/time', methods=['GET'])
def get_server_time():
    return jsonify({"server_time": datetime.utcnow().isoformat() + "Z"})

@app.route('/agendamentos', methods=['GET'])
def list_agendamentos():
    agendamentos = Agendamento.query.all()
    output = []
    for ag in agendamentos:
        data = ag.to_dict()
        data['_links'] = {
            'self': {'href': f"/agendamentos/{ag.id}"},
            'cancel': {'href': f"/agendamentos/{ag.id}/cancel", 'method': 'DELETE'}
        }
        output.append(data)
    return jsonify(output)

# NOVO: Cancelamento
@app.route('/agendamentos/<int:id>/cancel', methods=['DELETE'])
def cancel_agendamento(id):
    agendamento = Agendamento.query.get(id)
    if not agendamento:
        return jsonify({"message": "Agendamento não encontrado."}), 404

    detalhes_log = agendamento.to_dict()
    db.session.delete(agendamento)
    db.session.commit()
    
    logger.info(f"Agendamento {id} cancelado com sucesso.")

    audit_log = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "level": "AUDIT",
        "event_type": "AGENDAMENTO_CANCELADO",
        "service": "servico-agendamento",
        "details": detalhes_log
    }
    logger.audit(json.dumps(audit_log))

    return jsonify({"message": "Agendamento cancelado com sucesso."}), 200

# NOVO: Rota para o Site
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)