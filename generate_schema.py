import json

from schedule import app

with open("openapi.json", "w") as f:
    api_spec = app.openapi()
    f.write(json.dumps(api_spec, indent=2))
