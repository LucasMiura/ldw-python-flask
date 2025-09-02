# Importando o Flask
from flask import Flask, render_template

# Criando uma instancia do Flask
# __name__ representa o nome da aplicação
app = Flask(__name__, template_folder='views')

# Definindo uma rota principal da aplicação '/'


@app.route('/')
def home():  # Função que será executada ao acessar a rota
    return render_template('index.html')


@app.route('/games')
def games():
    title = 'Tarisland'
    year = 2022
    category = 'MMORPG'
    # Lista em Python (array)
    players = ['Yan', 'Ferrari', 'Valéria', 'Amanda']
    # Dicionário em Python (objeto)
    console = {
        'Nome': 'PlayStation 5',
        'Fabricante': 'Sony',
        'Ano': 2020
    }
    return render_template('games.html', title=title, year=year, category=category, players=players, console=console)


# Se for executado diretamente pelo interpretador
if __name__ == '__main__':
    # Iniciando o servidor
    app.run(host='localhost', port=5000, debug=True)
