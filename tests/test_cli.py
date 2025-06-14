import sys, pathlib, json
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from forgeengine.cli import load_config


def test_load_config_file(tmp_path):
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps({"memory": "x.json", "think": 1, "model": "m", "max_tokens": 5}))
    data = load_config(str(cfg))
    assert data["memory"] == "x.json"
    assert data["think"] == 1


