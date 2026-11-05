import sys

from products import PRODUCTS


def validate_products():
    if not PRODUCTS:
        raise ValueError("The product catalog must not be empty.")

    product_ids = [product["id"] for product in PRODUCTS]
    if len(product_ids) != len(set(product_ids)):
        raise ValueError("Product IDs must be unique.")

    required_fields = {"id", "name", "category", "description", "price"}
    for product in PRODUCTS:
        missing_fields = required_fields - product.keys()
        if missing_fields:
            raise ValueError(
                f"Product {product.get('id', '<unknown>')} is missing: "
                f"{', '.join(sorted(missing_fields))}"
            )
        if not product["name"].strip() or not product["category"].strip():
            raise ValueError(f"Product {product['id']} needs a name and category.")
        if product["price"] < 0:
            raise ValueError(f"Product {product['id']} has a negative price.")


if __name__ == "__main__":
    try:
        validate_products()
    except (KeyError, TypeError, ValueError) as error:
        print(f"Product validation failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(f"Validated {len(PRODUCTS)} products.")
