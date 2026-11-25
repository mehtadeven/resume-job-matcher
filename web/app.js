// Resume-Job Matcher - browser version of matcher.py.
// Same steps: TF-IDF ranks the job post's key terms, then we check which of
// them appear in the resume; cosine similarity gives an overall score.
// Everything runs in your browser - the text never leaves this page.

const SKLEARN_STOPS = new Set(SKLEARN_STOP_WORDS);
const CUSTOM_STOPS = new Set(CUSTOM_STOP_WORDS);

// matcher.clean_words: lowercase word tokens (keeps + # . for C++, C#, Node.js)
function cleanWords(text) {
  return String(text).toLowerCase().match(/[a-z][a-z0-9+#.]*/g) || [];
}

// Python's round(x, digits): rounds the exact binary value, ties go to the even digit
// (round(3.25, 1) == 3.2), so the numbers here match the Python output exactly.
function pyRound(x, digits = 1) {
  const exact = Math.abs(x).toFixed(30);
  const [whole, frac] = exact.split(".");
  const kept = whole + frac.slice(0, digits);
  const rest = frac.slice(digits).replace(/0+$/, "");
  let n = BigInt(kept);
  if (rest > "5" || (rest === "5" && n % 2n === 1n)) n += 1n;
  return (Math.sign(x) || 1) * Number(n) / 10 ** digits;
}
const round1 = (x) => pyRound(x, 1);

// matcher.text_similarity: TF-IDF cosine similarity, 0 to 100
function textSimilarity(resumeText, jobText) {
  try {
    const model = Tfidf.fit([jobText, resumeText], SKLEARN_STOPS);
    return round1(Tfidf.dot(model.rows[0], model.rows[1]) * 100);
  } catch {
    return 0; // nothing but stop words
  }
}

// matcher.keyword_report: split the job's top terms into found / missing
function keywordReport(resumeText, jobText, topN = 15) {
  let model;
  try {
    model = Tfidf.fit([jobText], SKLEARN_STOPS);
  } catch {
    return { found: [], missing: [] };
  }
  const row = model.rows[0];
  const scores = model.vocab.map((_, i) => row.get(i) || 0);
  const keywords = Tfidf.rankDesc(scores)
    .map((i) => model.vocab[i])
    .filter((term) => !CUSTOM_STOPS.has(term))
    .slice(0, topN);
  const resumeWords = new Set(cleanWords(resumeText));
  return {
    found: keywords.filter((w) => resumeWords.has(w)),
    missing: keywords.filter((w) => !resumeWords.has(w)),
  };
}

function analyse(resumeText, jobText) {
  const { found, missing } = keywordReport(resumeText, jobText);
  const total = found.length + missing.length;
  const coverage = total ? round1((100 * found.length) / total) : 0;
  return { found, missing, total, coverage, similarity: textSimilarity(resumeText, jobText) };
}

// ---- Page wiring (browser only) ----
if (typeof document !== "undefined") {
  const $ = (id) => document.getElementById(id);
  const resume = $("resume");
  const job = $("job");
  const out = $("result");

  function chips(target, words, cls) {
    target.innerHTML = "";
    if (!words.length) {
      target.innerHTML = '<span class="empty">none</span>';
      return;
    }
    for (const word of words) {
      const chip = document.createElement("span");
      chip.className = "chip " + cls;
      chip.textContent = word;
      target.appendChild(chip);
    }
  }

  function run() {
    if (!resume.value.trim() || !job.value.trim()) {
      out.hidden = true;
      return;
    }
    const r = analyse(resume.value, job.value);
    out.hidden = false;
    $("coverage").textContent = r.coverage.toFixed(1) + "%";
    $("coverage-detail").textContent = `${r.found.length} of ${r.total} job keywords found`;
    $("coverage-bar").style.width = r.coverage + "%";
    $("similarity").textContent = r.similarity.toFixed(1) + "%";
    $("similarity-bar").style.width = Math.min(100, r.similarity) + "%";
    $("found-count").textContent = r.found.length;
    $("missing-count").textContent = r.missing.length;
    chips($("found"), r.found, "good");
    chips($("missing"), r.missing, "bad");
    out.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  $("sample").addEventListener("click", () => {
    resume.value = SAMPLE_RESUME;
    job.value = SAMPLE_JOB;
    run();
  });
  $("clear").addEventListener("click", () => {
    resume.value = "";
    job.value = "";
    out.hidden = true;
    resume.focus();
  });
  $("check").addEventListener("click", run);

  resume.value = SAMPLE_RESUME;
  job.value = SAMPLE_JOB;
  run();
}

if (typeof module !== "undefined") module.exports = { cleanWords, textSimilarity, keywordReport, analyse };
