from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/nomedobanco'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

# Inicializando o banco de dados e migrações
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelos de banco de dados

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    tarefas = db.relationship('Tarefa', backref='usuario', lazy=True)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    setor = db.Column(db.String(100), nullable=False)
    prioridade = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='a fazer', nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

# Rotas

@app.route('/')
def home():
    return redirect(url_for('cadastro_usuario'))

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        usuario = Usuario(nome=nome, email=email)
        db.session.add(usuario)
        db.session.commit()
        flash("Cadastro de usuário realizado com sucesso!")
        return redirect(url_for('cadastro_usuario'))
    return render_template('cadastro_usuario.html')

@app.route('/cadastro_tarefa', methods=['GET', 'POST'])
def cadastro_tarefa():
    usuarios = Usuario.query.all()  # Recuperando usuários cadastrados
    if request.method == 'POST':
        descricao = request.form['descricao']
        setor = request.form['setor']
        prioridade = request.form['prioridade']
        usuario_id = request.form['usuario_id']
        
        tarefa = Tarefa(descricao=descricao, setor=setor, prioridade=prioridade, usuario_id=usuario_id)
        db.session.add(tarefa)
        db.session.commit()
        flash("Cadastro de tarefa realizado com sucesso!")
        return redirect(url_for('gerenciar_tarefas'))
    return render_template('cadastro_tarefa.html', usuarios=usuarios)

@app.route('/gerenciar_tarefas', methods=['GET', 'POST'])
def gerenciar_tarefas():
    tarefas_a_fazer = Tarefa.query.filter_by(status='a fazer').all()
    tarefas_fazendo = Tarefa.query.filter_by(status='fazendo').all()
    tarefas_pronto = Tarefa.query.filter_by(status='pronto').all()
    
    return render_template('gerenciar_tarefas.html', 
                           tarefas_a_fazer=tarefas_a_fazer, 
                           tarefas_fazendo=tarefas_fazendo, 
                           tarefas_pronto=tarefas_pronto)

@app.route('/atualizar_status/<int:tarefa_id>', methods=['POST'])
def atualizar_status(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    novo_status = request.form['status']
    tarefa.status = novo_status
    db.session.commit()
    flash(f"Status da tarefa alterado para {novo_status}!")
    return redirect(url_for('gerenciar_tarefas'))

if __name__ == '__main__':
    app.run(debug=True)
