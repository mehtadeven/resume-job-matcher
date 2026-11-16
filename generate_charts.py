"""
Generate the README result chart for the Resume-Job Matcher.

Runs matcher.py's real keyword report on the sample resume and job
description in this repo, and saves the coverage chart to
assets/result.png.

Run:  python generate_charts.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from matcher import keyword_report, text_similarity

NAVY = "#0B3C5D"
GOLD = "#E3A82B"
CREAM = "#F7F1E1"
BASE = Path(__file__).parent
OUT = BASE / "assets" / "result.png"


def main() -> None:
    resume_text = (BASE / "sample_resume.txt").read_text(encoding="utf-8")
    job_text = (BASE / "sample_job.txt").read_text(encoding="utf-8")

    found, missing = keyword_report(resume_text, job_text)
    total = len(found) + len(missing)
    coverage = round(100 * len(found) / total, 1) if total else 0.0
    similarity = text_similarity(resume_text, job_text)
    print(f"Keyword coverage: {coverage}% ({len(found)} of {total})")
    print(f"Text similarity: {similarity}%")
    print(f"Found: {', '.join(found)}")
    print(f"Missing: {', '.join(missing)}")

    fig, ax = plt.subplots(figsize=(8, 4.6))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    counts = [len(found), len(missing)]
    bars = ax.bar(["Found in resume", "Missing from resume"], counts,
                  color=[NAVY, GOLD], width=0.5)
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, count + 0.2,
                str(count), ha="center", fontsize=14, fontweight="bold")
    ax.set_ylim(0, max(counts) + 2)
    ax.set_ylabel("Job keywords (of 15 checked)")
    ax.set_title(f"Sample run — keyword coverage {coverage}%  |  text similarity {similarity}%",
                 fontsize=12, fontweight="bold", color=NAVY)
    fig.text(0.5, 0.01,
             f"Missing: {', '.join(missing)}",
             ha="center", fontsize=9, color="#374151")
    plt.tight_layout(rect=(0, 0.05, 1, 1))
    OUT.parent.mkdir(exist_ok=True)
    plt.savefig(OUT, dpi=150)
    print(f"Chart saved to {OUT}")


if __name__ == "__main__":
    main()
