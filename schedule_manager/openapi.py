from pathlib import Path

from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import (
    OpenAPIToolset,
)

from config import config

with (Path(config.openapi_schema_base_dir) / Path("openapi.json")).open("r") as f:
    openapi_spec_str = f.read()

toolset = OpenAPIToolset(spec_str=openapi_spec_str, spec_str_type="json")
