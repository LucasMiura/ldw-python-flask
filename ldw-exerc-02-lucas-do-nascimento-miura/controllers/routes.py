from flask import render_template, request, redirect, url_for
import urllib.request
import json
from models.database import Cloth, db

def init_app(app):
    produtos = []
    clientes = []

    # ------------------ PÁGINA INICIAL ------------------
    @app.route("/")
    def index():
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
    @app.route('/apiclothes', methods=['GET','POST'])
    @app.route('/apiclothes/<int:id>', methods=['GET','POST'])
    def apiclothes(id=None): 
        url = "https://fakestoreapi.com/products/category/men%27s%20clothing"
        response = urllib.request.urlopen(url)
        data = response.read()
        clothesList = json.loads(data)
        if id:
            clothInfo = []
            for cloth in clothesList:
                if cloth['id'] == id:
                    clothInfo = cloth
                    break
            if clothInfo:
                return render_template('clothinfo.html', clothInfo=clothInfo)
            else:
                return f'Roupa com a ID {id} não foi encontrada.'
        else:
            return render_template('apiclothes.html', clothesList = clothesList)

    # ------------------ ESTOQUE DE ROUPAS (CRUD) ------------------
    @app.route('/estoque_clothes', methods=['GET', 'POST'])
    @app.route('/estoque_clothes/delete/<int:id>')
    def estoque_clothes(id=None):
        if id:
            cloth = Cloth.query.get(id)
            db.session.delete(cloth)
            db.session.commit()
            return redirect(url_for('estoque_clothes'))
        
        if request.method == 'POST':
            newCloth = Cloth(
                request.form['title'],
                float(request.form['price']),
                request.form['category'],
                request.form['image']
            )
            db.session.add(newCloth)
            db.session.commit()
            return redirect(url_for('estoque_clothes'))
        
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
            cloth.price = float(request.form.get('price', cloth.price))
            cloth.category = request.form.get('category', cloth.category)
            cloth.image = request.form.get('image', cloth.image)
            db.session.commit()
            return redirect(url_for('estoque_clothes'))

        return render_template('editcloth.html', cloth=cloth)
