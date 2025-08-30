from flask import render_template, request, redirect, url_for


def init_app(app):
    players = ['yan', 'ferrari', 'valeria', 'amanda']
    gamelist = [{'Título': 'Slime Rancher',
                 'Ano': 2015, 'Categoria': 'Casual'}]

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