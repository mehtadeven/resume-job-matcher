import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from matcher import keyword_report, text_similarity

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


def test_empty_resume_finds_nothing():
    found, missing = keyword_report("", JOB)
    assert found == []
    assert len(missing) > 0
