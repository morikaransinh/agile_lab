import hmac
import os

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

from pricing import calculate_final_price
from products import PRODUCTS


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "local-demo-secret-change-before-deploying"),
        DEMO_USERNAME=os.environ.get("DEMO_USERNAME", "demo"),
        DEMO_PASSWORD=os.environ.get("DEMO_PASSWORD", "demo123"),
    )
    app.jinja_env.globals["calculate_final_price"] = calculate_final_price

    @app.get("/")
    def product_list():
        return render_template("index.html", products=PRODUCTS, query="", category="")

    @app.get("/products/<product_id>")
    def product_detail(product_id):
        product = next((item for item in PRODUCTS if item["id"] == product_id), None)
        if product is None:
            abort(404)
        return render_template("product_detail.html", product=product)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            username_matches = hmac.compare_digest(
                username, str(app.config["DEMO_USERNAME"])
            )
            password_matches = hmac.compare_digest(
                password, str(app.config["DEMO_PASSWORD"])
            )
            if username_matches and password_matches:
                session["username"] = username
                return redirect(url_for("dashboard"))
            flash("Invalid username or password.", "error")
        return render_template("login.html")

    @app.get("/dashboard")
    def dashboard():
        if "username" not in session:
            return redirect(url_for("login"))
        return render_template("dashboard.html", username=session["username"])

    @app.post("/logout")
    def logout():
        session.clear()
        return redirect(url_for("product_list"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
