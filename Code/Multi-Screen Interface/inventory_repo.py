import csv
CSV_PATH = "inventory.csv"

def load_inventory():
    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            temp = []
            for row in csv.DictReader(f):
                temp.append({
                    "id": int(row["id"]),
                    "name": row["name"],
                    "category": row["category"],
                    "price": float(row["price"]),
                    "quantity": int(row["quantity"])
                })
            return temp
    except FileNotFoundError:
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "name", "category", "price", "quantity"])
            writer.writeheader()
        return []

def save_inventory(items):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "category", "price", "quantity"])
        writer.writeheader()
        for item in items:
            writer.writerow({
                "id": item["id"],
                "name": item["name"],
                "category": item["category"],
                "price": item["price"],
                "quantity": item["quantity"]
            })