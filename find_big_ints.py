import json

LIMIT = 2147483647

with open("data_utf8.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for obj in data:
    if obj.get("model") == "deliverycompany.deliverycompany":
        fields = obj.get("fields", {})
        for key, value in fields.items():
            if isinstance(value, int) and abs(value) > LIMIT:
                print("MODEL:", obj.get("model"))
                print("FIELD:", key)
                print("VALUE:", value)
                print("-" * 40)
