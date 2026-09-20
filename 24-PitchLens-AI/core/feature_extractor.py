"""
Feature Extractor Module for PitchLens AI
Extracts keyword patterns, pitch section presence flags, n-grams, and quantitative evidence.
"""
import re
import logging
from typing import Dict, Any, List, Set, Tuple

logger = logging.getLogger("PitchLens.FeatureExtractor")


class FeatureExtractor:
    """Extracts linguistic, structural, domain-specific, and quantitative features from pitch text."""

    # Keyword lexicons for pitch component detection
    KEYWORDS = {
        "problem": [
            "problem", "pain point", "inefficiency", "waste", "struggle", "challenge", 
            "issue", "costly", "burnout", "frustration", "lack of", "fragmented", 
            "manual", "delayed", "expensive", "loss", "risk"
        ],
        "solution": [
            "solution", "platform", "product", "software", "agent", "tool", "app", 
            "system", "technology", "automates", "solves", "provides", "delivers", 
            "algorithm", "ai-powered", "patent", "device"
        ],
        "market": [
            "market", "tam", "sam", "som", "addressable market", "industry", "sector", 
            "global market", "billion", "million", "customers", "target audience", 
            "merchants", "practices", "schools", "enterprises"
        ],
        "customer": [
            "customer", "user", "client", "buyer", "developer", "doctor", "farmer", 
            "exporter", "retailer", "freight operator", "physician", "patient", 
            "consumer", "subscriber", "merchant", "smb", "enterprise"
        ],
        "business_model": [
            "business model", "monetize", "revenue model", "subscription", "saas", 
            "license", "fee", "margin", "pricing", "pay-per-use", "freemium", 
            "commission", "transaction fee", "recurring revenue", "arr", "mrr"
        ],
        "revenue": [
            "revenue", "mrr", "arr", "sales", "monetization", "cash flow", "income", 
            "gross margin", "net margin", "off-take"
        ],
        "pricing": [
            "pricing", "price", "charge", "$", "₹", "per month", "per year", "per user", 
            "per acre", "per endpoint", "per shipment", "per doctor", "tier"
        ],
        "competition": [
            "competitor", "competition", "alternative", "unlike", "compared to", "versus", 
            "vs", "traditional", "existing solutions", "differentiate", "advantage", 
            "moat", "crowdstrike", "nuance", "instacart", "swift"
        ],
        "usp": [
            "unique", "differentiation", "moat", "competitive advantage", "1-click", 
            "10x", "zero downtime", "patented", "proprietary", "integrated", "native"
        ],
        "traction": [
            "traction", "customers", "users", "pilots", "pilot", "revenue", "mrr", 
            "processed", "growth", "active", "subscribers", "retention", "ltv", 
            "completed", "deployed", "orders", "volume", "arr"
        ],
        "prototype": [
            "prototype", "mvp", "demo", "beta", "pilot", "launch", "testing", "deployed"
        ],
        "team": [
            "team", "founder", "co-founder", "ceo", "cto", "architect", "engineer", 
            "alumni", "ex-google", "ex-aws", "phd", "veteran", "expert", "experience", 
            "doctor", "professor", "stanford", "harvard", "mit"
        ],
        "technology": [
            "technology", "ai", "ml", "nlp", "cloud", "serverless", "api", "microservice", 
            "lorawan", "iot", "lidar", "stablecoin", "hipaa", "soc2", "blockchain"
        ],
        "scalability": [
            "scalable", "scalability", "scale", "expansion", "architecture", "distributed", 
            "cloud-native", "expansion", "automation", "depot", "global"
        ],
        "roadmap": [
            "roadmap", "timeline", "future", "milestone", "expand", "q1", "q2", "q3", 
            "q4", "next year", "expansion"
        ],
        "financial": [
            "financial", "financials", "cac", "ltv", "margin", "payback", "runway", 
            "fundraising", "raise", "valuation", "profitability", "unit economics"
        ]
    }

    @classmethod
    def extract_presence_flags(cls, text: str) -> Dict[str, bool]:
        """
        Detect presence of key pitch sections and concepts based on keyword lexicons.
        Returns a dict of boolean flags (e.g. {'problem_present': True, ...}).
        """
        text_lower = text.lower()
        flags = {}
        for category, keywords in cls.KEYWORDS.items():
            flag_name = f"{category}_present"
            found = any(re.search(r"\b" + re.escape(kw) + r"\b", text_lower) for kw in keywords)
            flags[flag_name] = found
        return flags

    @classmethod
    def extract_quantitative_evidence(cls, text: str) -> Dict[str, Any]:
        """
        Extract numerical and quantitative metrics from pitch text:
        - Numbers, percentages, currency, revenue, users, market sizes, timeline references.
        """
        evidence = {
            "has_quantitative_evidence": False,
            "currency_mentions": [],
            "percentage_mentions": [],
            "user_metric_mentions": [],
            "revenue_mentions": [],
            "market_size_mentions": [],
            "raw_numbers_count": 0,
            "evidence_snippets": [],
        }

        if not text:
            return evidence

        # Extract Currency Mentions (e.g. $30B, ₹4.2 lakh, $499/mo, $500k, €100k)
        currency_pattern = r"(?:[\$₹€]\s?\d+(?:\.\d+)?\s*(?:b|m|k|billion|million|thousand|crore|lakh)?|\b\d+(?:\.\d+)?\s*(?:dollars|rupees|usd|inr)\b)"
        currencies = re.findall(currency_pattern, text, flags=re.IGNORECASE)
        evidence["currency_mentions"] = [c.strip() for c in currencies]

        # Extract Percentages (e.g. 18% MoM, 82% gross margin, 94% physician score, 43%)
        pct_pattern = r"\b\d+(?:\.\d+)?%|\b\d+(?:\.\d+)?\s*percent\b"
        percentages = re.findall(pct_pattern, text, flags=re.IGNORECASE)
        evidence["percentage_mentions"] = [p.strip() for p in percentages]

        # Extract User/Customer Count Mentions (e.g. 45 customers, 2,500 developers, 15,000 encounters, 1,200 farmers)
        user_pattern = r"\b\d{1,3}(?:,\d{3})*|\d+(?:\.\d+)?[kM]?\s*(?:customers|users|clients|developers|doctors|farmers|exporters|endpoints|subscribers|merchants|pilots|families|riders|encounters)\b"
        users = re.findall(user_pattern, text, flags=re.IGNORECASE)
        evidence["user_metric_mentions"] = [u.strip() for u in users if any(char.isdigit() for char in u)]

        # Extract Revenue/Financial Metrics (e.g. MRR, ARR, LTV/CAC, gross margin)
        revenue_pattern = r"\b(?:mrr|arr|ltv|cac|gross margin|payback|revenue|volume)\b"
        rev_terms = re.findall(revenue_pattern, text, flags=re.IGNORECASE)
        evidence["revenue_mentions"] = list(set(rev_terms))

        # Extract Market Size Mentions (TAM, SAM, SOM)
        market_pattern = r"\b(?:tam|sam|som|addressable market)\b"
        mkt_terms = re.findall(market_pattern, text, flags=re.IGNORECASE)
        evidence["market_size_mentions"] = list(set(mkt_terms))

        # Count general numbers in text
        all_numbers = re.findall(r"\b\d+(?:\,\d{3})*(?:\.\d+)?\b", text)
        evidence["raw_numbers_count"] = len(all_numbers)

        # Flag overall quantitative strength
        if currencies or percentages or users or (len(all_numbers) >= 3):
            evidence["has_quantitative_evidence"] = True

        # Extract sentence snippets containing quantitative proof
        sentences = re.split(r"(?<=[.!?])\s+", text)
        snippets = []
        for s in sentences:
            if re.search(r"[\$₹%]|mrr|arr|tam|sam|gross margin|clients|customers|revenue|profit|users", s, flags=re.IGNORECASE):
                snippets.append(s.strip())
        evidence["evidence_snippets"] = snippets[:5]

        return evidence

    @classmethod
    def extract_ngrams(cls, words: List[str], n: int = 2) -> List[str]:
        """Generate word n-grams (unigrams, bigrams, trigrams)."""
        if len(words) < n:
            return []
        return [" ".join(words[i : i + n]) for i in range(len(words) - n + 1)]

    @classmethod
    def get_all_features(cls, text: str) -> Dict[str, Any]:
        """Comprehensive feature dictionary combining section flags and quantitative signals."""
        presence_flags = cls.extract_presence_flags(text)
        quant_evidence = cls.extract_quantitative_evidence(text)
        return {
            "presence_flags": presence_flags,
            "quantitative_evidence": quant_evidence,
        }
