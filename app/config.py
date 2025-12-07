import tomllib
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "settings.toml"

with open(CONFIG_PATH, "rb") as f:
    config = tomllib.load(f)

server_config = config["server"]
model_config = config["model"]

db_type = "csv" # csv or database
csv_data_path = Path(__file__).parent.parent / "temp_table"
