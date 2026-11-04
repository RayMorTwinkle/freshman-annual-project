import csv, json, platform
from pathlib import Path
values = [int(row["value"]) for row in csv.DictReader(Path("/content/annual_cli_input.csv").open())]
experiment_total = sum(values)
result = {"sum": experiment_total, "count": len(values), "python": platform.python_version()}
Path("/content/annual_cli_result.json").write_text(json.dumps(result))
print(json.dumps(result))
