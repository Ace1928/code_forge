import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from forgeengine.engine import NarrativeEngine


def test_engine_response(tmp_path):
    engine = NarrativeEngine(
        memory_path=str(tmp_path / "mem.json"),
        model_name="sshleifer/tiny-gpt2",
    )
    response = engine.respond("hello")
    assert "hello" in response


