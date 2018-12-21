import json

# Define of Elements
types = ["Bible Snippet", "Praise", "Worship", "Gospel"]

# Writing on file
json.dump(types, open("../static/json/types.json", "w"))

# Notfication that data is dumped
print("dumped")
