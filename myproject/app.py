from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Usuario, Tarefa

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

migrate = Migrate(app, db)  

# Rota para a página inicial
@app.route('/') 
def home():
    return redirect(url_for('cadastro_usuario'))  # Redireciona para a página de cadastro de usuários


# Rota de cadastro de usuário
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

# Rota de cadastro de tarefa
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

# Rota para gerenciar tarefas
@app.route('/gerenciar_tarefas', methods=['GET', 'POST'])
def gerenciar_tarefas():
    tarefas_a_fazer = Tarefa.query.filter_by(status='a fazer').all()
    tarefas_fazendo = Tarefa.query.filter_by(status='fazendo').all()
    tarefas_pronto = Tarefa.query.filter_by(status='pronto').all()
    
    return render_template('gerenciar_tarefas.html', tarefas_a_fazer=tarefas_a_fazer, 
                           tarefas_fazendo=tarefas_fazendo, tarefas_pronto=tarefas_pronto)

# Rota para editar tarefa
@app.route('/editar_tarefa/<int:tarefa_id>', methods=['GET', 'POST'])
def editar_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    usuarios = Usuario.query.all()
    if request.method == 'POST':
        tarefa.descricao = request.form['descricao']
        tarefa.setor = request.form['setor']
        tarefa.prioridade = request.form['prioridade']
        tarefa.usuario_id = request.form['usuario_id']
        
        db.session.commit()
        flash("Tarefa atualizada com sucesso!")
        return redirect(url_for('gerenciar_tarefas'))
    return render_template('editar_tarefa.html', tarefa=tarefa, usuarios=usuarios)

# Rota para excluir tarefa
@app.route('/excluir_tarefa/<int:tarefa_id>', methods=['POST'])
def excluir_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    db.session.delete(tarefa)
    db.session.commit()
    flash("Tarefa excluída com sucesso!")
    return redirect(url_for('gerenciar_tarefas'))

# Rota para atualizar status da tarefa
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
