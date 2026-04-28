"""
responder.py — LLM response layer for Rural Scheme Navigator
=============================================================
Takes eligibility results + user profile and generates a
structured, grounded, human-readable response.

GenAI concept: PROMPT ENGINEERING + GROUNDING
  The LLM is never asked to recall schemes from memory.
  It only receives retrieved + rule-filtered scheme data
  and is instructed to format and explain — not invent.

  Grounding strategy:
    - System prompt forbids adding information not in context
    - All scheme facts come from EligibilityResult objects
    - LLM role: plain English explainer, not knowledge source

Two modes:
  1. LOCAL  — Ollama running Mistral-7B on your machine (free, private)
  2. API    — HuggingFace Inference API (free tier, needs token)

Set MODE in config below. Defaults to a rule-based fallback
if neither is available — so the app always returns something.

Usage:
    from llm.responder import SchemeResponder
    responder = SchemeResponder()
    response  = responder.generate(user_profile, eligible_results)
"""

import os
import json
import requests
from dataclasses import asdict
from engine.eligibility import EligibilityResult, UserProfile

# ── Config ──
# Options: "ollama" | "hf_api" | "rule_based"
# Start with "rule_based" — no setup needed, always works
# Switch to "ollama" once you have Ollama installed
MODE = os.getenv("SCHEME_LLM_MODE", "rule_based")

# Ollama settings (if MODE = "ollama")
OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

# HuggingFace settings (if MODE = "hf_api")
# Get free token at huggingface.co/settings/tokens
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_MODEL  = "mistralai/Mistral-7B-Instruct-v0.2"
HF_URL    = f"https://api-inference.huggingface.co/models/{HF_MODEL}"


class SchemeResponder:
    """
    Generates plain-English scheme guidance grounded in
    retrieved + eligibility-filtered scheme data.
    """

    def generate(
        self,
        profile: UserProfile,
        results: list[EligibilityResult],
        max_schemes: int = 3,
    ) -> dict:
        """
        Generate a full response for the user.

        Args:
            profile:     user's profile
            results:     eligibility results from EligibilityEngine
            max_schemes: max eligible schemes to explain in detail

        Returns:
            dict with keys:
              summary        — one paragraph overview
              schemes        — list of scheme response dicts
              no_results_msg — set if no eligible schemes found
        """
        eligible = [r for r in results if r.eligible][:max_schemes]
        ineligible = [r for r in results if not r.eligible]

        if not eligible:
            return {
                "summary": self._no_results_summary(profile),
                "schemes": [],
                "no_results_msg": (
                    "No schemes matched your profile from the current results. "
                    "Try broadening your search or check eligibility manually "
                    "at myscheme.gov.in"
                ),
            }

        scheme_responses = []
        for result in eligible:
            scheme_response = self._explain_scheme(profile, result)
            scheme_responses.append(scheme_response)

        summary = self._generate_summary(profile, eligible)

        return {
            "summary":        summary,
            "schemes":        scheme_responses,
            "ineligible_count": len(ineligible),
            "no_results_msg": None,
        }

    # ────────────────────────────────────────
    # Rule-based response builders
    # These always work — no LLM needed
    # ────────────────────────────────────────

    def _explain_scheme(
        self,
        profile: UserProfile,
        result: EligibilityResult,
    ) -> dict:
        """
        Build a structured scheme explanation.
        Uses LLM only for the plain-English summary paragraph.
        All facts come from the EligibilityResult — no hallucination possible.
        """
        # Build the plain-English eligibility explanation (rule-based)
        eligibility_explanation = self._build_eligibility_explanation(result)

        # Optionally enhance the summary with LLM
        llm_summary = self._llm_summarise(profile, result)

        return {
            "scheme_name":             result.scheme_name,
            "scheme_id":               result.scheme_id,
            "category":                result.category,
            "state":                   result.state,
            "ministry":                result.ministry,
            "eligible":                result.eligible,
            "confidence":              result.confidence,

            # Why the user is eligible — from rules
            "eligibility_explanation": eligibility_explanation,

            # Warnings to flag to user
            "warnings":                result.warnings,

            # Scheme details — directly from retrieved data
            "what_you_get":            result.benefits,
            "benefit_amount":          result.benefit_amount,

            # Documents needed
            "documents_needed":        result.documents,

            # Step-by-step application guide
            "how_to_apply":            result.apply_steps,

            # Portal link
            "apply_url":               result.apply_url,

            # Plain-English summary (LLM or rule-based fallback)
            "plain_summary":           llm_summary,
        }

    def _build_eligibility_explanation(self, result: EligibilityResult) -> str:
        """
        Build a clear, plain-English explanation of why the user
        is eligible. Purely rule-based — zero hallucination risk.
        """
        parts = []

        if result.reasons:
            parts.append("You qualify because: " + "; ".join(result.reasons) + ".")
        if result.warnings:
            parts.append("Please note: " + "; ".join(result.warnings) + ".")

        if not parts:
            return "You appear to meet the basic eligibility criteria for this scheme."

        return " ".join(parts)

    def _generate_summary(
        self,
        profile: UserProfile,
        eligible: list[EligibilityResult],
    ) -> str:
        """One-paragraph summary of all eligible schemes found."""
        names = [r.scheme_name for r in eligible]
        count = len(names)

        profile_desc = []
        if profile.occupation:
            profile_desc.append(profile.occupation.lower())
        if profile.state:
            profile_desc.append(f"from {profile.state}")
        if profile.caste_category:
            profile_desc.append(f"({profile.caste_category} category)")

        profile_str = " ".join(profile_desc) if profile_desc else "your profile"

        if count == 1:
            return (
                f"Based on your profile as a {profile_str}, "
                f"we found 1 scheme you are eligible for: {names[0]}."
            )
        scheme_list = ", ".join(names[:-1]) + f", and {names[-1]}"
        return (
            f"Based on your profile as a {profile_str}, "
            f"we found {count} schemes you are eligible for: {scheme_list}."
        )

    def _no_results_summary(self, profile: UserProfile) -> str:
        return (
            f"We could not find matching schemes for your current profile. "
            f"This may be because the query did not retrieve relevant schemes, "
            f"or your profile does not meet the eligibility criteria of the "
            f"schemes in our current database. Try visiting myscheme.gov.in "
            f"directly for a complete search."
        )

    # ────────────────────────────────────────
    # LLM integration (optional enhancement)
    # ────────────────────────────────────────

    def _llm_summarise(
        self,
        profile: UserProfile,
        result: EligibilityResult,
    ) -> str:
        """
        Generate a 2-3 sentence plain-English summary of the scheme
        for this specific user. Falls back to rule-based if LLM unavailable.

        GenAI concept: PROMPT ENGINEERING
          The prompt is structured to:
          1. Give the LLM a clear role (plain-language explainer)
          2. Provide all facts as context (grounding)
          3. Forbid adding information not in context
          4. Specify exact output format (2-3 sentences, simple English)
        """
        if MODE == "rule_based":
            return self._rule_based_summary(profile, result)
        elif MODE == "ollama":
            return self._ollama_summarise(profile, result)
        elif MODE == "hf_api":
            return self._hf_summarise(profile, result)
        else:
            return self._rule_based_summary(profile, result)

    def _build_prompt(self, profile: UserProfile, result: EligibilityResult) -> str:
        """
        Structured prompt for LLM.

        Grounding strategy:
          - All scheme facts are injected directly into the prompt
          - Explicit instruction: only use the information provided
          - Output constrained to 2-3 sentences in simple English
          - No open-ended generation — LLM formats, not invents
        """
        profile_str = (
            f"Age: {profile.age or 'not specified'}, "
            f"State: {profile.state or 'not specified'}, "
            f"Occupation: {profile.occupation or 'not specified'}, "
            f"Caste: {profile.caste_category or 'not specified'}, "
            f"Gender: {profile.gender or 'not specified'}, "
            f"Annual income: Rs. {profile.annual_income or 'not specified'}"
        )

        scheme_facts = (
            f"Scheme name: {result.scheme_name}\n"
            f"What you get: {result.benefits}\n"
            f"Benefit amount: {result.benefit_amount or 'varies'}\n"
            f"Ministry: {result.ministry}\n"
            f"Why eligible: {'; '.join(result.reasons) if result.reasons else 'meets basic criteria'}"
        )

        return f"""[INST] You are a helpful government scheme advisor for rural India.
Your job is to explain a government scheme to a specific person in simple, clear English.

USER PROFILE:
{profile_str}

SCHEME INFORMATION (use ONLY this information — do not add anything else):
{scheme_facts}

Write 2-3 sentences explaining:
1. What this scheme gives the user specifically
2. Why they are eligible
3. One practical tip for applying

Use simple English. Do not mention any scheme or fact not listed above. [/INST]"""

    def _rule_based_summary(
        self,
        profile: UserProfile,
        result: EligibilityResult,
    ) -> str:
        """
        Build a clean plain-English summary using only simple sentences.
        Avoids scheme names and acronyms so Hindi translation works cleanly.
        """
        amount  = result.benefit_amount or "financial assistance"
        category_sentences = {
            "Agriculture":               "This scheme gives direct financial support to farmers every year.",
            "Housing":                   "This scheme helps you build a pucca house with government money.",
            "Employment":                "This scheme provides guaranteed work and wages to rural families.",
            "Financial Inclusion":       "This scheme gives you access to a free bank account and insurance.",
            "Health":                    "This scheme covers your hospital expenses at no cost to you.",
            "Education":                 "This scheme helps pay for your education through a low interest loan.",
            "Financial Assistance":      "This scheme provides a loan or grant to help start your livelihood.",
            "Social Security":           "This scheme protects your family with insurance at a very low cost.",
            "Social Welfare":            "This scheme provides essential support to improve your daily life.",
            "Skill Development":         "This scheme trains you for free and helps you find better work.",
            "Women and Child Development":"This scheme provides financial support for women and girl children.",
            "Infrastructure":            "This scheme improves roads and connectivity in your village.",
        }

        base = category_sentences.get(
            result.category,
            "This scheme provides government support that you are eligible for."
        )

        eligibility_line = ""
        if profile.occupation:
            eligibility_line = f"You are eligible as a {profile.occupation.lower()}"
            if profile.state:
                eligibility_line += f" from {profile.state}"
            eligibility_line += "."

        amount_line = f"You can receive {amount} if you apply successfully."

        return f"{base} {eligibility_line} {amount_line}".strip()
        

    def _ollama_summarise(
        self,
        profile: UserProfile,
        result: EligibilityResult,
    ) -> str:
        """Call local Ollama instance (Mistral-7B)."""
        prompt = self._build_prompt(profile, result)
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model":  OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,   # Low temp = more factual, less creative
                        "num_predict": 150,   # Limit output length
                    }
                },
                timeout=30,
            )
            data = response.json()
            return data.get("response", "").strip()
        except Exception as e:
            print(f"Ollama error: {e} — falling back to rule-based summary")
            return self._rule_based_summary(profile, result)

    def _hf_summarise(
        self,
        profile: UserProfile,
        result: EligibilityResult,
    ) -> str:
        """Call HuggingFace Inference API (free tier)."""
        if not HF_TOKEN:
            return self._rule_based_summary(profile, result)

        prompt = self._build_prompt(profile, result)
        try:
            response = requests.post(
                HF_URL,
                headers={"Authorization": f"Bearer {HF_TOKEN}"},
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 150,
                        "temperature":    0.3,
                        "return_full_text": False,
                    }
                },
                timeout=30,
            )
            data = response.json()
            if isinstance(data, list):
                return data[0].get("generated_text", "").strip()
            return self._rule_based_summary(profile, result)
        except Exception as e:
            print(f"HF API error: {e} — falling back to rule-based summary")
            return self._rule_based_summary(profile, result)


# ── Standalone test ──
if __name__ == "__main__":
    from rag.retriever import SchemeRetriever
    from engine.eligibility import EligibilityEngine

    retriever = SchemeRetriever()
    engine    = EligibilityEngine()
    responder = SchemeResponder()

    profile = UserProfile(
        age=35,
        annual_income=80000,
        state="Bihar",
        occupation="farmer",
        gender="Male",
        caste_category="SC",
        residence="Rural",
        has_land=True,
        has_bank_account=True,
    )

    query   = "schemes for farmers in Bihar"
    chunks  = retriever.retrieve(query, k=5)
    results = engine.check(profile, chunks)
    response = responder.generate(profile, results)

    print(f"\nSUMMARY:\n{response['summary']}\n")
    print(f"{'='*60}")

    for scheme in response["schemes"]:
        print(f"\nScheme: {scheme['scheme_name']}")
        print(f"Category: {scheme['category']} | State: {scheme['state']}")
        print(f"Confidence: {scheme['confidence']}")
        print(f"\nEligibility: {scheme['eligibility_explanation']}")
        print(f"\nWhat you get: {scheme['what_you_get']}")
        print(f"Benefit amount: {scheme['benefit_amount']}")
        print(f"\nDocuments needed:")
        for doc in scheme["documents_needed"]:
            print(f"  - {doc}")
        print(f"\nHow to apply:")
        for i, step in enumerate(scheme["how_to_apply"], 1):
            print(f"  {i}. {step}")
        print(f"\nApply at: {scheme['apply_url']}")
        print(f"\nSummary: {scheme['plain_summary']}")
        print(f"{'='*60}")