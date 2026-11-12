from __future__ import annotations

import re
import sys
from pathlib import Path
from types import SimpleNamespace


DOCUMENT = Path("terraform/ssm-remediation/main.tf")


def inline_script() -> str:
    """Extract the Python source embedded in the Automation document."""
    content = DOCUMENT.read_text(encoding="utf-8")
    match = re.search(r"^          Script: \|-\r?\n((?:^            .*\r?\n?)*)", content, re.MULTILINE)
    assert match, "The Automation document must contain an inline script."
    return "\n".join(line.removeprefix("            ") for line in match.group(1).splitlines())


def test_inline_automation_handler_is_a_function_name_and_dry_run_does_not_write(monkeypatch) -> None:
    content = DOCUMENT.read_text(encoding="utf-8")
    assert "Handler: handler" in content
    assert "Handler: script.handler" not in content

    writes: list[dict[str, object]] = []

    class FakeS3:
        def put_public_access_block(self, **kwargs: object) -> None:
            writes.append(kwargs)

    monkeypatch.setitem(sys.modules, "boto3", SimpleNamespace(client=lambda _service: FakeS3()))
    namespace: dict[str, object] = {}
    exec(inline_script(), namespace)

    result = namespace["handler"]({"BucketName": "dry-run-bucket", "DryRun": "true"}, None)

    assert result == {"status": "WOULD_REMEDIATE", "bucket": "dry-run-bucket"}
    assert writes == []


def test_inline_automation_handler_has_ssm_execute_script_signature() -> None:
    script = inline_script()
    assert "def handler(events, context):" in script
    assert "'status': 'WOULD_REMEDIATE'" in script
