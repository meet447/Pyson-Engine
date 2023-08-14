import json

# Load JSON data
def load_json(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print("Error loading JSON:", e)
        return None
