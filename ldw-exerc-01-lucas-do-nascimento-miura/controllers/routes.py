from flask import render_template, request, redirect, url_for

def init_app(app):
    produtos = []
    clientes = []

    # Página inicial
    @app.route("/")
    def index():
        return render_template("index.html")

    # Rota de produtos (lista)
    @app.route("/produtos", methods=["GET", "POST"])
    def page_produtos():
        if request.method == "POST":
            nome = request.form.get("nome")
            if nome:
                produtos.append(nome)
            return redirect(url_for("page_produtos"))
        return render_template("produtos.html", produtos=produtos)

    # Rota de clientes (dicionário -> tabela)
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
