import glob, json, pathlib
from ruamel.yaml import YAML
from pymongo import MongoClient, ASCENDING
from jsonschema import validate, ValidationError

yaml = YAML(typ="safe")

SRC_DIR = pathlib.Path("marker_yml")          # Original-Ordner
SCHEMA_DIR = pathlib.Path("schemas")          # JSON-Schemata
REGISTRY = pathlib.Path("DETECT_registry.json")

client = MongoClient("mongodb://localhost:27017")
db     = client["lean_deep"]

# 1) Indexe für neue Sammlungen
for col in ("markers_atomic", "markers_semantic", "markers_cluster", "markers_meta"):
    db[col].create_index([("id", ASCENDING)], unique=True)

prefix_col = {
    "ATO_": "markers_atomic",
    "SEM_": "markers_semantic",
    "CLU_": "markers_cluster",
    "MEMA_": "markers_meta",
}

# 2) LD3.2-Schema laden
SCHEMA_PATH = SCHEMA_DIR / "marker.schema.v3.json"
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    marker_schema = json.load(f)

def validate_marker_schema(marker_dict):
    try:
        validate(instance=marker_dict, schema=marker_schema)
        return True
    except ValidationError as e:
        print(f"❌ Schema-Fehler für {marker_dict.get('id', 'UNBEKANNT')}: {e}")
        return False

# 3) Marker-Import
for f in SRC_DIR.glob("**/*.y*ml"):
    data = yaml.load(f.read_text(encoding="utf-8"))
    if not data or "id" not in data:
        print(f"⚠️  skip (no id): {f}")
        continue

    # Präfix prüfen / reparieren
    if data["id"].startswith(("A_", "S_", "C_", "MM_")):
        mapping = {"A_":"ATO_", "S_":"SEM_", "C_":"CLU_", "MM_":"MEMA_"}
        data["id"] = mapping[data["id"][:2]] + data["id"][2:]
    prefix = data["id"][:4]
    if prefix not in prefix_col:
        print(f"🚫  invalid prefix: {data['id']}")
        continue

    data["_id"] = data["id"]
    if not validate_marker_schema(data):
        print(f"🚫 Marker wird nicht importiert: {data['id']}")
        continue

    collection  = db[prefix_col[prefix]]
    collection.replace_one({"_id": data["_id"]}, data, upsert=True)
    print(f"✓ {data['_id']} → {collection.name}")

# 4) Schemata einlesen
for sf in SCHEMA_DIR.glob("*.json"):
    sch = json.loads(sf.read_text(encoding="utf-8"))
    db.schemas.replace_one({"_id": sch["id"]}, sch, upsert=True)

# 5) Detector-Registry
registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
for det in registry:
    db.detectors.replace_one({"_id": det["id"]}, det, upsert=True)

print("Lean-Deep 3.4 DB ready 🏁")
