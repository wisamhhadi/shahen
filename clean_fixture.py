import json
from collections import Counter

input_file = "data_utf8.json"
output_file = "data_clean.json"

exclude_models = {
    "deliverycompany.deliverycompanytoken",
    "authtoken.token",
}

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

counts = Counter(obj.get("model") for obj in data)

clean_data = [
    obj for obj in data
    if obj.get("model") not in exclude_models
]

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(clean_data, f, ensure_ascii=False, indent=2)

print("Original objects:", len(data))
print("Clean objects:", len(clean_data))
print("Removed objects:", len(data) - len(clean_data))
print("Removed deliverycompany tokens:", counts.get("deliverycompany.deliverycompanytoken", 0))
print("Removed authtoken tokens:", counts.get("authtoken.token", 0))
print("Created:", output_file)
