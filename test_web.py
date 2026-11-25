
from decimal import Decimal

from playwright.sync_api import Page


BASE_URL = "https://www.saucedemo.com/"


def check_result(description, expected, actual):
    """Výpis očekávaného a skutečného výsledku a jejich porovnání."""
    print(f"\n{description}")
    print(f"Expected: {expected}")
    print(f"Actual:   {actual}")
    assert actual == expected, description
    print("Result: PASS")


def login(page: Page):
    """Přihlášení pomocí veřejného testovacího účtu."""
    page.goto(BASE_URL)
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    page.locator(".inventory_list").wait_for(state="visible")

    check_result(
        "Login - inventory page",
        BASE_URL + "inventory.html",
        page.url,
    )


def read_products(page: Page):
    """Načtení názvů a cen produktů v aktuálním pořadí."""
    products = []

    for item in page.locator(".inventory_item").all():
        name = item.locator(".inventory_item_name").inner_text()
        price_text = item.locator(".inventory_item_price").inner_text()
        price = Decimal(price_text.replace("$", ""))
        products.append((name, price))

    assert products, "Seznam produktů je prázdný."
    return products


def read_cart(page: Page):
    """Kontrola množství a načtení obsahu košíku nebo rekapitulace."""
    result = {}

    for item in page.locator(".cart_item").all():
        name = item.locator(".inventory_item_name").inner_text()
        price_text = item.locator(".inventory_item_price").inner_text()
        price = Decimal(price_text.replace("$", ""))

        check_result(
            f"Quantity - {name}",
            "1",
            item.locator(".cart_quantity").inner_text(),
        )

        assert name not in result, f"Duplicate product: {name}"
        result[name] = price

    return result


def read_amount(page: Page, selector: str):
    """Převod zobrazené peněžní částky na desetinné číslo."""
    text = page.locator(selector).inner_text()
    return Decimal(text.split("$")[-1])


def test_checkout_validation(page: Page):
    """TC01 - Validace povinných objednávkových údajů."""
    print("\n=== TC01: Checkout validation ===")

    login(page)
    page.locator("#add-to-cart-sauce-labs-backpack").click()
    page.locator(".shopping_cart_link").click()
    page.locator("#checkout").click()

    error = page.locator('[data-test="error"]')

    # Postupné ověření všech povinných údajů.
    for field, value, message in [
        ("#first-name", "Jan", "Error: First Name is required"),
        ("#last-name", "Novak", "Error: Last Name is required"),
        ("#postal-code", "40001", "Error: Postal Code is required"),
    ]:
        page.locator("#continue").click()
        error.wait_for(state="visible")

        check_result(
            f"Validation message - {field}",
            message,
            error.inner_text(),
        )

        check_result(
            "Checkout page remains unchanged",
            BASE_URL + "checkout-step-one.html",
            page.url,
        )

        page.locator(field).fill(value)
        print(f"Input entered: {field} = {value}")

    # Po doplnění všech údajů musí být možné pokračovat.
    page.locator("#continue").click()
    page.locator(".summary_info").wait_for(state="visible")

    check_result(
        "Checkout with all required fields completed",
        BASE_URL + "checkout-step-two.html",
        page.url,
    )


def test_product_sorting(page: Page):
    """TC02 - Řazení produktů a ověření integrity dat."""
    print("\n=== TC02: Product sorting ===")

    login(page)
    original = read_products(page)

    print("\nOriginal product catalogue:")
    for name, price in original:
        print(f"{name}: ${price}")

    print(f"Original product count: {len(original)}")
    assert len(original) >= 2
    assert len({price for _, price in original}) >= 2

    sort = page.locator(".product_sort_container")

    # Kontrola obou směrů řazení a zachování produktových dat.
    for option, descending in [("lohi", False), ("hilo", True)]:
        direction = "Descending" if descending else "Ascending"

        sort.select_option(option)
        current = read_products(page)
        prices = [price for _, price in current]

        print(f"\n{direction} product catalogue:")
        for name, price in current:
            print(f"{name}: ${price}")

        check_result(
            f"{direction} price order",
            sorted(prices, reverse=descending),
            prices,
        )

        check_result(
            f"{direction} product count",
            len(original),
            len(current),
        )

        check_result(
            f"{direction} product data integrity",
            sorted(original),
            sorted(current),
        )


def test_complete_purchase(page: Page):
    """TC03 - Kompletní nákupní proces s kontrolou objednávky."""
    print("\n=== TC03: Complete purchase ===")

    login(page)
    products = dict(read_products(page))

    selected = {
        "Sauce Labs Backpack": "sauce-labs-backpack",
        "Sauce Labs Bike Light": "sauce-labs-bike-light",
        "Sauce Labs Bolt T-Shirt": "sauce-labs-bolt-t-shirt",
    }

    # Přidání tří produktů do košíku.
    print("\nSelected products:")
    for name, product_id in selected.items():
        print(f"{name}: ${products[name]}")
        page.locator(f"#add-to-cart-{product_id}").click()

    badge = page.locator(".shopping_cart_badge")

    check_result(
        "Cart badge after adding products",
        "3",
        badge.inner_text(),
    )

    page.locator(".shopping_cart_link").click()

    check_result(
        "Shopping cart page",
        BASE_URL + "cart.html",
        page.url,
    )

    # Odstranění jednoho produktu z košíku.
    page.locator("#remove-sauce-labs-bike-light").click()
    print("\nRemoved product: Sauce Labs Bike Light")

    check_result(
        "Cart badge after removing product",
        "2",
        badge.inner_text(),
    )

    del selected["Sauce Labs Bike Light"]
    expected = {name: products[name] for name in selected}

    check_result(
        "Shopping cart contents",
        expected,
        read_cart(page),
    )

    # Vyplnění objednávkových údajů.
    page.locator("#checkout").click()
    page.locator("#first-name").fill("Jan")
    page.locator("#last-name").fill("Novak")
    page.locator("#postal-code").fill("40001")

    print("\nCheckout data: Jan, Novak, 40001")

    page.locator("#continue").click()
    page.locator(".summary_info").wait_for(state="visible")

    check_result(
        "Checkout overview page",
        BASE_URL + "checkout-step-two.html",
        page.url,
    )

    check_result(
        "Checkout overview contents",
        expected,
        read_cart(page),
    )

    # Kontrola mezisoučtu, daně a celkové ceny.
    subtotal = sum(expected.values(), Decimal("0.00"))
    displayed_subtotal = read_amount(
        page, ".summary_subtotal_label"
    )
    tax = read_amount(page, ".summary_tax_label")
    total = read_amount(page, ".summary_total_label")

    check_result(
        "Order subtotal",
        subtotal,
        displayed_subtotal,
    )

    print(f"\nDisplayed tax: ${tax}")

    check_result(
        "Tax is non-negative",
        True,
        tax >= Decimal("0.00"),
    )

    check_result(
        "Order total",
        subtotal + tax,
        total,
    )

    # Dokončení simulované objednávky.
    page.locator("#finish").click()
    confirmation = page.locator(".complete-header")
    confirmation.wait_for(state="visible")

    check_result(
        "Order confirmation",
        "Thank you for your order!",
        confirmation.inner_text(),
    )

    check_result(
        "Order confirmation page",
        BASE_URL + "checkout-complete.html",
        page.url,
    )

    check_result(
        "Cart badge visibility after purchase",
        False,
        badge.is_visible(),
    )
