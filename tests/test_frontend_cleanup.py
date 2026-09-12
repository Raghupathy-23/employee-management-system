from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_employee_lookup_limit_does_not_exceed_api_maximum():
    for filename in ("src/pages/Attendance.jsx", "src/pages/Leaves.jsx"):
        text = (ROOT / filename).read_text(encoding="utf-8")
        assert "limit: 200" not in text
        assert "limit: 100" in text
