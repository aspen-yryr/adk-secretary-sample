import json
from pathlib import Path

from config import config
from schedule import app

with (Path(config.openapi_schema_base_dir) / Path("openapi.json")).open("w") as f:
    api_spec = app.openapi()
    f.write(json.dumps(api_spec, indent=2))
