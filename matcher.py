"""Resume-Job Matcher.

Compares a resume with a job description using TF-IDF and cosine
similarity, then reports the match score and which important job
keywords are present in the resume and which are missing.
"""

import re
import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Words too common to count as skills or keywords.
STOP_WORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "with",
    "on", "at", "is", "are", "we", "you", "will", "our", "your",
    "work", "team", "experience", "years", "year", "looking", "join",
    "role", "job", "candidate", "skills", "skill", "knowledge",
    "build", "clean", "clear", "pull", "collaborate", "help", "using",
    "use", "used", "write", "run", "track", "prepare", "ship", "hiring",
    "plus", "good", "strong", "small", "real", "helping", "tasks",
    "responsibilities", "requirements", "familiarity", "understanding",
    "fundamentals", "basics", "intern", "products", "services",
    "experiments", "reports", "habits", "communication", "documentation",
}


def clean_words(text):
    """Return the lowercase word tokens of a text."""
    return re.findall(r"[a-z][a-z0-9+#.]*", text.lower())


def text_similarity(resume_text, job_text):
    """Return the TF-IDF cosine similarity of the two texts, from 0 to 100."""
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform([job_text, resume_text])
    score = cosine_similarity(matrix[0], matrix[1])[0][0]
    return round(float(score) * 100, 1)


def keyword_report(resume_text, job_text, top_n=15):
    """Split the job's key terms into (found_in_resume, missing)."""
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform([job_text])
    scores = matrix.toarray()[0]
    terms = vectorizer.get_feature_names_out()

    # Rank job terms by TF-IDF weight, keep the meaningful ones.
    ranked = sorted(zip(terms, scores), key=lambda pair: pair[1], reverse=True)
    keywords = [term for term, _ in ranked if term not in STOP_WORDS][:top_n]

    resume_words = set(clean_words(resume_text))
    found = [word for word in keywords if word in resume_words]
    missing = [word for word in keywords if word not in resume_words]
    return found, missing


def main():
    if len(sys.argv) != 3:
        print("Usage: python matcher.py <resume.txt> <job.txt>")
        return
    resume_text = open(sys.argv[1], encoding="utf-8").read()
    job_text = open(sys.argv[2], encoding="utf-8").read()

    found, missing = keyword_report(resume_text, job_text)
    total = len(found) + len(missing)
    coverage = round(100 * len(found) / total, 1) if total else 0.0
    similarity = text_similarity(resume_text, job_text)

    print(f"Keyword coverage: {coverage}%  ({len(found)} of {total} job keywords found)")
    print(f"Overall text similarity: {similarity}%")
    print(f"\nKeywords you have ({len(found)}):")
    print("  " + (", ".join(found) if found else "none"))
    print(f"\nKeywords missing ({len(missing)}):")
    print("  " + (", ".join(missing) if missing else "none"))


if __name__ == "__main__":
    main()
