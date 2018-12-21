import json

# Define of Elements
types = ["name", "content", "description"]

# Writing on file
json.dump(types, open("../static/json/snippets_columns.json", "w"))

# Notfication that data is dumped
print("dumped")
