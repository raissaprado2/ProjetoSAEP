from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    # Relacionamento com Tarefa
    tarefas = db.relationship('Tarefa', backref='usuario', lazy=True)


class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    setor = db.Column(db.String(100), nullable=False)
    prioridade = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='a fazer', nullable=False)

    # Chave estrangeira para a tabela Usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)





