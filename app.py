"""Tiny web UI for the Resume-Job Matcher.

Run:  python app.py
Open: http://localhost:8000

Uses only Python's built-in web server - no extra packages to install.
Paste a resume and a job description, and it shows the keyword
coverage, the text similarity, and the keywords still missing.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from matcher import keyword_report, text_similarity

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Resume-Job Matcher</title>
<style>
  body { font-family: Arial, sans-serif; margin: 2rem auto; max-width: 900px; padding: 0 1rem; }
  h1 { color: #0b3c5d; }
  textarea { width: 100%; height: 180px; margin-bottom: 1rem; }
  button { background: #0b3c5d; color: #fff; border: 0; padding: 0.7rem 1.4rem; cursor: pointer; }
  .score { font-size: 1.6rem; font-weight: bold; color: #0b3c5d; }
  .found { color: #157347; } .missing { color: #b02a37; }
</style>
</head>
<body>
<h1>Resume-Job Matcher</h1>
<p>Paste your resume and a job description. The tool compares them with
TF-IDF and shows which job keywords your resume already covers.</p>
<form method="post">
  <label>Your resume</label>
  <textarea name="resume" required>%%RESUME%%</textarea>
  <label>Job description</label>
  <textarea name="job" required>%%JOB%%</textarea>
  <button type="submit">Check my match</button>
</form>
%%RESULT%%
</body>
</html>"""


def render(resume, job, result):
    """Fill the page template (plain replace, so CSS braces stay safe)."""
    return (PAGE.replace("%%RESUME%%", resume)
                .replace("%%JOB%%", job)
                .replace("%%RESULT%%", result))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._send(render("", "", ""))

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        fields = parse_qs(self.rfile.read(length).decode("utf-8"))
        resume = fields.get("resume", [""])[0]
        job = fields.get("job", [""])[0]

        found, missing = keyword_report(resume, job)
        total = len(found) + len(missing)
        coverage = round(100 * len(found) / total, 1) if total else 0.0
        similarity = text_similarity(resume, job)

        result = f"""
        <p class="score">Keyword coverage: {coverage}% ({len(found)} of {total})</p>
        <p>Overall text similarity: {similarity}%</p>
        <p class="found"><b>You have:</b> {", ".join(found) or "none"}</p>
        <p class="missing"><b>Missing:</b> {", ".join(missing) or "none"}</p>
        <p>Add the missing skills to your resume only if you truly have them -
        the goal is an honest resume that passes the first screening.</p>"""
        self._send(render(resume, job, result))

    def _send(self, html):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print("Open http://localhost:8000 in your browser")
    HTTPServer(("localhost", 8000), Handler).serve_forever()
