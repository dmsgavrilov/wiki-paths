import json
import os

DB_PATH = "db/db.txt"

try:
    os.mkdir("db")
except:
    pass


with open(DB_PATH, "w") as f:
    json.dump({"results": []}, f)


def read():
    with open(DB_PATH, "r") as f:
        results = json.load(f)["results"]
    return results


def write(obj):
    with open(DB_PATH, "w") as f:
        json.dump({"results": obj}, f)
