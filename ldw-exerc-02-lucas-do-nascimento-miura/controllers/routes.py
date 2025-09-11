from flask import render_template, request, redirect, url_for
import urllib.request
import urllib.parse
import json
from models.database import Cloth, db

def init_app(app):
    produtos = []
    clientes = []

    # ------------------ PÁGINA INICIAL ------------------
    @app.route("/")
    def home():
        return render_template("index.html")

    # ------------------ PRODUTOS ------------------
    @app.route("/produtos", methods=["GET", "POST"])
    def page_produtos():
        if request.method == "POST":
            nome = request.form.get("nome")
            if nome:
                produtos.append(nome)
            return redirect(url_for("page_produtos"))
        return render_template("produtos.html", produtos=produtos)

    # ------------------ CLIENTES ------------------
    @app.route("/clientes", methods=["GET", "POST"])
    def page_clientes():
        if request.method == "POST":
            nome = request.form.get("nome")
            email = request.form.get("email")
            telefone = request.form.get("telefone")
            cpf = request.form.get("cpf")

            if nome and email and telefone and cpf:
                clientes.append({
                    "nome": nome,
                    "email": email,
                    "telefone": telefone,
                    "cpf": cpf
                })
                return redirect(url_for("page_clientes"))

        return render_template("clientes.html", clientes=clientes)

    # ------------------ API DE ROUPAS ------------------
    @app.route('/apiclothes', methods=['GET'])
    @app.route('/apiclothes/<int:id>', methods=['GET'])
    def apiclothes(id=None):
        # Definindo todas as categorias
        categories = ["men's clothing", "women's clothing", "jewelery"]

        all_clothes = []

        # Loop para buscar produtos de todas as categorias
        for cat in categories:
            url = f"https://fakestoreapi.com/products/category/{urllib.parse.quote(cat)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})  # utilizado para evitar 403
            response = urllib.request.urlopen(req)
            data = response.read()
            all_clothes.extend(json.loads(data))

        # Busca um item específico
        if id:
            cloth_info = next((c for c in all_clothes if c['id'] == id), None)
            if cloth_info:
                return render_template('clothinfo.html', clothInfo=cloth_info)
            else:
                return f"Roupa com ID {id} não encontrada.", 404

        # Mostra todos os produtos
        return render_template('apiclothes.html', clothesList=all_clothes)

    # ------------------ ESTOQUE DE ROUPAS (CRUD) ------------------
    @app.route('/estoque_clothes', methods=['GET', 'POST'])
    @app.route('/estoque_clothes/delete/<int:id>')
    def estoque_clothes(id=None):
        # Exclusão: valida existência antes de deletar
        if id:
            cloth = Cloth.query.get(id)
            if not cloth:
                return f"Roupa com ID {id} não encontrada.", 404
            db.session.delete(cloth)
            db.session.commit()
            return redirect(url_for('estoque_clothes'))

        # Cadastro
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            price_raw = request.form.get('price', '0').strip()
            category = request.form.get('category', '').strip()
            image = request.form.get('image', '').strip()
            quantity_raw = request.form.get('quantity', '0').strip()

            # conversões
            try:
                price = float(price_raw) if price_raw else 0.0
            except ValueError:
                price = 0.0

            try:
                quantity = int(quantity_raw) if quantity_raw else 0
            except ValueError:
                quantity = 0

            if not image:
                # placeholder caso não forneça imagem
                image = "https://via.placeholder.com/300x300?text=Sem+Imagem"

            newCloth = Cloth(title, price, category, image, quantity)
            db.session.add(newCloth)
            db.session.commit()
            return redirect(url_for('estoque_clothes'))

        # Listagem
        clothesEstoque = Cloth.query.all()
        return render_template('estoque_clothes.html', clothesEstoque=clothesEstoque)

    # ------------------ EDITAR ROUPAS (CRUD) ------------------
    @app.route('/edit_cloth/<int:id>', methods=['GET', 'POST'])
    def edit_cloth(id):
        cloth = Cloth.query.get(id)
        if not cloth:
            return f"Roupa com ID {id} não encontrada.", 404

        if request.method == 'POST':
            # Atualiza os campos da roupa
            cloth.title = request.form.get('title', cloth.title)
            try:
                cloth.price = float(request.form.get('price', cloth.price))
            except ValueError:
                # mantém o valor anterior caso haja erro de conversão
                pass
            cloth.category = request.form.get('category', cloth.category)
            cloth.image = request.form.get('image', cloth.image)
            # quantity (int)
            try:
                cloth.quantity = int(request.form.get('quantity', cloth.quantity))
            except ValueError:
                pass

            db.session.commit()
            return redirect(url_for('estoque_clothes'))

        return render_template('editcloth.html', cloth=cloth)
