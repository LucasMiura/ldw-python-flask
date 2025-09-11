from flask import Flask
from controllers import routes
from models.database import db
import os

app = Flask(__name__, template_folder="views")

# Inicializa as rotas
routes.init_app(app)

# Extraindo o diretório absoluto do arquivo
dir = os.path.abspath(os.path.dirname(__file__))

# Configuração do banco SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models', 'clothes.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



if __name__ == "__main__":
    # Inicializa o banco com a app
    db.init_app(app)

    # Cria as tabelas, se não existirem
    with app.app_context():
        db.create_all()
    
    # Iniciando servidor
    app.run(host="0.0.0.0", port=4000, debug=True)
