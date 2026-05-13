from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__,)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    senha = db.Column(db.String(15))

    def __init__(self, email, senha):
        self.email = email
        self.senha = senha


# Garante que o comando seja executado dentro do contexto do seu app Flask
with app.app_context():
    db.create_all()
    print("Banco de dados criado com sucesso!")

#PARA TELA LOGIN

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Pega o que o usuário digitou na SUA tela de login
        email_digitado = request.form.get("email") 
        senha_digitada = request.form.get("senha")
        
        # Procura no banco de dados
        user = Usuario.query.filter_by(email=email_digitado).first()
        
        if user and user.senha == senha_digitada:
            return "Login realizado com sucesso! Bem-vindo ao sistema."
        else:
            return "Erro: E-mail ou senha não encontrados no banco."
            
    return render_template("login.html") # Sua tela original


#TELA DE CADASTRO

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        # Pega os dados da SUA tela de cadastro
        email = request.form.get("email")
        senha = request.form.get("senha")
        
        # SALVA NO BANCO (O "esquelético" SQLite)
        novo_usuario = Usuario(email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        
        # Após salvar, ele te joga de volta para a SUA tela de login
        return redirect(url_for('login'))
        
    return render_template("cadastro.html") # Sua tela de cadastro

if __name__ == '__main__':
    app.run(debug=True)