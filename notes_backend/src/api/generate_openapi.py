import json
import os

from src.api.main import app

# Generate and persist the OpenAPI schema to the interfaces directory so that
# external consumers (e.g., frontend) can rely on it.
openapi_schema = app.openapi()

output_dir = "interfaces"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openapi.json")

with open(output_path, "w") as f:
    json.dump(openapi_schema, f, indent=2)
