from pathlib import Path

source = Path("data.json")
target = Path("data_utf8.json")

raw = source.read_bytes()

encodings = [
    "utf-8-sig",
    "utf-16",
    "cp1256",
    "windows-1256",
    "cp1252",
    "latin1",
]

for enc in encodings:
    try:
        text = raw.decode(enc)
        target.write_text(text, encoding="utf-8")
        print(f"Converted successfully using encoding: {enc}")
        print(f"Created: {target}")
        break
    except UnicodeDecodeError:
        pass
else:
    raise SystemExit("Could not decode data.json with common encodings")
