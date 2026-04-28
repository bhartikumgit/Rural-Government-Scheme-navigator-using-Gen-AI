"""
app.py — Flask web application for Rural Scheme Navigator
=========================================================
Two routes:
  GET  /        — profile input form
  POST /query   — runs full pipeline, returns results page

Full pipeline on each query:
  1. Parse user profile from form
  2. Build search query from profile
  3. RAG retrieval (FAISS + BM25)
  4. Eligibility engine (rule-based)
  5. Response generation
  6. Render results template
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# chatgpt said this
import math



from flask import Flask, render_template, request, jsonify
from rag.retriever import SchemeRetriever
from engine.eligibility import EligibilityEngine, UserProfile
from llm.responder import SchemeResponder
from translation.hindi import HindiTranslator
translator = HindiTranslator()

app = Flask(__name__)
@app.template_filter('cos_deg')
def cos_deg(angle):
    return math.cos(math.radians(angle))

@app.template_filter('sin_deg')
def sin_deg(angle):
    return math.sin(math.radians(angle))
# ── Load pipeline components once at startup ──
print("Loading pipeline...")
retriever = SchemeRetriever()
engine    = EligibilityEngine()
responder = SchemeResponder()
print("Pipeline ready.\n")


def build_query(profile: UserProfile) -> str:
    """
    Convert structured user profile into a natural language
    search query for the RAG retriever.
    """
    parts = []
    if profile.occupation:
        parts.append(f"schemes for {profile.occupation.lower()}")
    if profile.state:
        parts.append(f"in {profile.state}")
    if profile.caste_category in ("SC", "ST", "OBC"):
        parts.append(f"for {profile.caste_category} category")
    if profile.annual_income and profile.annual_income < 150000:
        parts.append("for low income families")
    if profile.gender == "Female":
        parts.append("for women")
    if not parts:
        parts.append("government welfare schemes India")
    return " ".join(parts)



@app.route("/")
def index():
    """Render the profile input form."""
    return render_template("index.html", errors=[])


@app.route("/query", methods=["POST"])
def query():
    try:
        age           = int(request.form.get("age", 0)) or None
        annual_income = int(request.form.get("annual_income", 0)) or None
    except ValueError:
        age = annual_income = None

    occupation = request.form.get("occupation", "").strip() or None
    state      = request.form.get("state", "").strip() or None

    # ── Server-side validation ──
    # Client-side alone is not enough — users can bypass HTML required attrs
    errors = []
    if not occupation:
        errors.append("Please select your occupation.")
    if not state:
        errors.append("Please select your state.")

    if errors:
        return render_template("index.html", errors=errors)

    profile = UserProfile(
        age              = age,
        annual_income    = annual_income,
        state            = state,
        occupation       = occupation,
        gender           = request.form.get("gender", "").strip() or None,
        caste_category   = request.form.get("caste_category", "").strip() or None,
        residence        = request.form.get("residence", "").strip() or None,
        has_land         = request.form.get("has_land") == "yes",
        has_bank_account = request.form.get("has_bank_account") == "yes",
    )

    search_query = build_query(profile)
    chunks       = retriever.retrieve(search_query, k=8)
    results      = engine.check(profile, chunks)
    response     = responder.generate(profile, results, max_schemes=5)
    

   
   # Translate all scheme fields using pre-translated static strings
    for scheme in response["schemes"]:
        scheme.update(translator.translate_scheme_response(scheme))
    if response.get("summary"):
        response["summary_hi"] = translator.translate(response["summary"])

    return render_template(
        "results.html",
        response=response,
        profile=profile,
        query=search_query,
    )

@app.route("/api/query", methods=["POST"])
def api_query():
    """
    JSON API endpoint — same pipeline as /query but returns JSON.
    Useful for testing and future mobile app integration.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    try:
        age           = int(data.get("age", 0)) or None
        annual_income = int(data.get("annual_income", 0)) or None
    except (ValueError, TypeError):
        age = annual_income = None

    profile = UserProfile(
        age            = age,
        annual_income  = annual_income,
        state          = data.get("state"),
        occupation     = data.get("occupation"),
        gender         = data.get("gender"),
        caste_category = data.get("caste_category"),
        residence      = data.get("residence"),
        has_land       = data.get("has_land", False),
        has_bank_account = data.get("has_bank_account", True),
    )

    search_query = build_query(profile)
    chunks       = retriever.retrieve(search_query, k=8)
    results      = engine.check(profile, chunks)
    response     = responder.generate(profile, results, max_schemes=5)

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)