from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__,)

# O XAMPP por padrão vem com o usuário 'root' e sem nenhuma senha (por isso fica vazio depois dos dois pontos)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/controle_ti'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    senha = db.Column(db.String(15))

    def __init__(self, email, senha):
        self.email = email
        self.senha = senha


class Equipamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    modelo = db.Column(db.String(100))
    # unique=True impede que salve duas séries iguais!
    serie = db.Column(db.String(50), unique=True) 
    sala = db.Column(db.String(50))    # Para mudar o equipamento de sala
    status = db.Column(db.String(50))  # Ex: "Ativo", "Em Manutenção", "Sucata"

    def __init__(self, tipo, modelo, serie, sala="Sala 01", status="Ativo"):
        self.tipo = tipo
        self.modelo = modelo
        self.serie = serie
        self.sala = sala
        self.status = status


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
            return redirect(url_for('dashboard'))
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


#TELA INICIAL

@app.route("/dashboard")
def dashboard():
    # Puxa todos os equipamentos salvos no banco de dados
    lista_do_banco = Equipamento.query.all()
    # Envia essa lista para dentro do HTML com o nome de 'equipamentos'
    return render_template("dashboard.html", equipamentos=lista_do_banco)

# ROTA PARA CADASTRAR EQUIPAMENTOS
# Mude de @app.route("/cadastrar_equipamento") para isto:
@app.route("/cadastrar_equipamento", methods=["GET", "POST"])
def cadastrar_equipamento():
    if request.method == "POST":
        # ... o resto do seu código que pega os dados e salva no banco ...
        # Pegando os dados do formulário rosa
        tipo = request.form.get("tipo") or ""
        modelo = request.form.get("modelo") or ""
        status = request.form.get("status") or ""
        serie = request.form.get("serie") or ""
        
        # Criando o objeto
        novo_item = Equipamento(tipo=tipo, modelo=modelo, status=status, serie=serie)
        
        # Salvando no banco
        db.session.add(novo_item)
        db.session.commit()
        
    # ATENÇÃO: Esse return fica alinhado com o 'if', fora dele!
    # Se terminar o POST ou se acontecer qualquer outra coisa, ele recarrega o dashboard
        return redirect(url_for('dashboard'))
    return render_template("novo_equipamento.html")

@app.route("/editar_equipamento/<int:id>", methods=["GET", "POST"])
def editar_equipamento(id):
    equipamento = Equipamento.query.get_or_404(id)
    
    if request.method == "POST":
        equipamento.tipo = request.form.get("tipo")
        equipamento.modelo = request.form.get("modelo")
        equipamento.serie = request.form.get("serie")
        # ESSA LINHA AQUI EMBAIXO É A CHAVE:
        equipamento.sala = request.form.get("sala") or "Sala 01"  
        equipamento.status = request.form.get("status") or "Ativo"
        
        db.session.commit()
        return redirect(url_for('dashboard'))
        
    return render_template("editar_equipamento.html", equipamento=equipamento)

if __name__ == '__main__':
    app.run(debug=True)