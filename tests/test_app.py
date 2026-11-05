from app import app
from products import PRODUCTS


def test_catalog_displays_all_products():
    response = app.test_client().get("/")

    assert response.status_code == 200
    for product in PRODUCTS:
        assert product["name"].encode() in response.data


def test_product_filter_searches_name_and_category():
    response = app.test_client().get("/?q=serum")

    assert response.status_code == 200
    assert b"Hydrating Serum" in response.data
    assert b"Everyday Shampoo" not in response.data


def test_product_filter_limits_results_to_category():
    response = app.test_client().get("/?category=Hair+Care")

    assert response.status_code == 200
    assert b"Everyday Shampoo" in response.data
    assert b"Daily Moisturizer" not in response.data


def test_product_filter_shows_empty_state_when_no_product_matches():
    response = app.test_client().get("/?q=not-a-product")

    assert response.status_code == 200
    assert b"No products found." in response.data


def test_product_detail_displays_product():
    response = app.test_client().get("/products/everyday-shampoo")

    assert response.status_code == 200
    assert b"Everyday Shampoo" in response.data


def test_unknown_product_returns_not_found():
    response = app.test_client().get("/products/not-a-product")

    assert response.status_code == 404


def test_dashboard_requires_login():
    response = app.test_client().get("/dashboard")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


def test_login_accepts_demo_credentials():
    client = app.test_client()
    response = client.post(
        "/login", data={"username": "demo", "password": "demo123"}
    )

    assert response.status_code == 302
    assert client.get("/dashboard").status_code == 200


def test_login_rejects_invalid_credentials():
    response = app.test_client().post(
        "/login", data={"username": "demo", "password": "wrong"}
    )

    assert response.status_code == 200
    assert b"Invalid username or password." in response.data
