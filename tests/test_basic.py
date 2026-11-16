import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from matcher import keyword_report, save_chart, text_similarity

RESUME = "Python developer with scikit-learn, pandas and classification experience."
JOB = "We need a Python developer with scikit-learn, Docker and SQL experience."


def test_identical_texts_are_fully_similar():
    assert text_similarity(JOB, JOB) == 100.0


def test_known_keywords_are_found():
    found, missing = keyword_report(RESUME, JOB)
    assert "python" in found
    assert "learn" in found or "scikit-learn" in found or "scikit" in found


def test_missing_keywords_are_reported():
    found, missing = keyword_report(RESUME, JOB)
    assert "docker" in missing
    assert "sql" in missing


def test_chart_flag_saves_a_png(tmp_path):
    chart_path = tmp_path / "chart.png"
    save_chart(["python", "git"], ["docker"], str(chart_path))
    assert chart_path.exists()
    assert chart_path.stat().st_size > 5_000  # a real chart, not an empty file


def test_empty_resume_finds_nothing():
    found, missing = keyword_report("", JOB)
    assert found == []
    assert len(missing) > 0
