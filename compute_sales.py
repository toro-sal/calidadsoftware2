"""Compute Sales Script.

This script processes sales data based on a given product catalog,
calculates total sales, logs errors, and appends results to a file.
It also runs linting checks using pylint and flake8.
"""
import json
import sys
import time
import os


def load_json(file_path):
    """Load a JSON file and return its contents."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}")
        return None


def normalize_product_catalogue(product_list):
    """Normalize the product catalogue to map titles to prices."""
    return {
        product["title"].lower(): product["price"]
        for product in product_list
    }


def compute_total_sales(price_catalogue, sales_record):
    """Compute the total cost of sales based on the catalogue."""
    total_cost = 0.0
    errors = []
    for sale in sales_record:
        product = sale.get("Product")
        quantity = sale.get("Quantity", 0)
        if not product:
            errors.append(f"Missing product name in sale entry: {sale}")
            continue
        product = product.lower()
        if product not in price_catalogue:
            errors.append(f"Invalid product: {product}")
            continue
        try:
            unit_price = price_catalogue[product]
            total_cost += unit_price * quantity
        except (TypeError, ValueError) as e:
            errors.append(f"Error processing sale {sale}: {e}")
    return total_cost, errors


def run_pylint():
    """Run PyLint on this script and append results to pylint_results.txt."""
    pylint_output = os.popen("pylint compute_sales.py").read()
    with open("pylint_results.txt", "a", encoding="utf-8") as pylint_file:
        pylint_file.write("\n" + "=" * 40 + "\n")
        pylint_file.write(" PyLint Results \n")
        pylint_file.write("=" * 40 + "\n")
        pylint_file.write(pylint_output)
        pylint_file.write("\n" + "=" * 40 + "\n")


def run_flake8():
    """Run Flake8 on this script and append results to flake8_results.txt."""
    flake8_output = os.popen("flake8 compute_sales.py").read()
    with open("flake8_results.txt", "a", encoding="utf-8") as flake8_file:
        flake8_file.write("\n" + "=" * 40 + "\n")
        flake8_file.write(" Flake8 Results \n")
        flake8_file.write("=" * 40 + "\n")
        flake8_file.write(flake8_output)
        flake8_file.write("\n" + "=" * 40 + "\n")


def process_sales(price_catalogue_file, sales_file):
    """Process a single sales file and append results with a separator."""
    price_catalogue_data = load_json(price_catalogue_file)
    sales_data = load_json(sales_file)
    if price_catalogue_data is None or sales_data is None:
        sys.exit(1)
    price_catalogue = normalize_product_catalogue(price_catalogue_data)
    start_time = time.time()
    total_cost, errors = compute_total_sales(price_catalogue, sales_data)
    elapsed_time = time.time() - start_time
    result_text = (
        "\n" + "=" * 40 + "\n"
        + f"Sales Report - Run on {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        + "=" * 40 + "\n"
        + f"Total Sales Cost: ${total_cost:.2f}\n"
        + f"Elapsed Time: {elapsed_time:.4f} seconds\n"
        + ("\nErrors:\n" + "\n".join(errors) if errors else "")
        + "\n" + "-" * 40 + "\n"
    )
    print(result_text)
    with open("SalesResults.txt", "a", encoding="utf-8") as file:
        file.write(result_text)
    print("Results appended in SalesResults.txt")


def main():
    """Main function to compute sales for a single test case."""
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py priceCatalogue.json "
              "salesRecord.json")
        sys.exit(1)
    price_file = sys.argv[1]
    sales_file = sys.argv[2]
    process_sales(price_file, sales_file)
    run_pylint()
    run_flake8()


if __name__ == "__main__":
    main()
