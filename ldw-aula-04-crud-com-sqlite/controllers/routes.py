from flask import render_template, request, redirect, url_for
import urllib # Envia requisições a uma URL
import json # Faz a conversão de dados json -> dicionário
# Importando o model de Game
from models.database import Game, db 


def init_app(app):
    # Lista em Python (array)
    players = ['yan', 'ferrari', 'valeria', 'amanda']
    # Array de objetos - Lista de jogos
    gamelist = [{'Título': 'Slime Rancher','Ano': 2015, 'Categoria': 'Casual'}]

    @app.route('/')
    def home():  # função que será executada ao acessar a rota
        return render_template('index.html')

    @app.route('/games', methods=['GET', 'POST'])
    def games():  # função que será executada ao acessar a rota
        title = 'Tarisland'
        year = 2022
        category = 'MMORPG'
        console = {'name': 'playstation 5',
                   'manufacturer': 'sony', 'year': 2020}
        # tratando um req post com request
        if request.method == 'POST':
            # coletando o texto da input
            if request.form.get('player'):
                players.append(request.form.get('player'))
                return redirect(url_for('games'))

        return render_template('games.html', title=title, year=year, category=category, players=players, console=console)

    @app.route('/newgame', methods=['GET', 'POST'])
    def newgame():

        if request.method == 'POST':
            if request.form.get('title') and request.form.get('year') and request.form.get('category'):
                gamelist.append({"Título": request.form.get('title'), "Ano": request.form.get(
                    'year'), "Categoria": request.form.get('category')})
                return redirect(url_for('newgame'))
        return render_template('newGame.html', gamelist=gamelist)
    
    @app.route('/apigames', methods=['GET','POST'])
    # Criando parâmetros para a rota
    @app.route('/apigames/<int:id>', methods=['GET','POST'])
    
    def apigames(id=None): # Parâmetro opcional
        url = 'https://www.freetogame.com/api/games'
        response = urllib.request.urlopen(url)
        data = response.read()
        gamesList = json.loads(data)
        # Verificando se o parâmetro foi enviado
        if id:
            gameInfo = []
            for game in gamesList:
                if game['id'] == id: # Comparando os IDs
                    gameInfo = game
                    break
            if gameInfo:
                return render_template('gameinfo.html', gameInfo=gameInfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'
        else:
            return render_template('apigames.html', gamesList = gamesList)
    
    # CRUD - Listagem e Cadastro
    @app.route('/estoque', methods=['GET', 'POST'])
    @app.route('/estoque/delete/<int:id>')
    def estoque(id=None):
        if id:
            # Seleciona o jogo pela ID
            game = Game.query.get(id)
            # Deleta o jogo pela ID
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque'))
        
        if request.method == 'POST':
            # Realiza o cadastro do jogo
            newGame = Game(request.form['title'], request.form['year'], request.form['category'], request.form['platform'], request.form['price'], request.form['quantity'])
            # .session.add é o método do SQLAlchemy para gravar registros no banco
            db.session.add(newGame)
            # .session.commit confirma as alterações no banco
            db.session.commit()
            return redirect(url_for('estoque'))
            
        else:
            # PAGINAÇÃO DE REGISTROS
            # Captura o valor de 'page' que foi passado pelo método GET
            page = request.args.get('page', 1, type=int)
            # Valor definido para registros em cada página
            per_page = 3
            # query.all é um método do SQL Alchemy para selecionar todos os registros
            # query.paginaete é o método para filtrar os registros de acordo com um limite
            gamesEstoque = Game.query.paginate(page=page, per_page=per_page)
            return render_template('estoque.html', gamesEstoque=gamesEstoque)
    
    # CRUD - Rota de EDIÇÃO
    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        game = Game.query.get(id)        
        if request.method == 'POST':
            game.title = request.form['title']
            game.year = request.form['year']
            game.category = request.form['category']
            game.platform = request.form['platform']
            game.price = request.form['price']
            game.quantity = request.form['quantity']
            db.session.commit()
            return redirect(url_for('estoque'))        
        return render_template('editgame.html', game=game)