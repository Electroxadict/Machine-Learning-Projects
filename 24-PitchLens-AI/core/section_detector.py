"""
Section Detector Module for PitchLens AI
Evaluates presence, completeness, and specific missing sub-elements for 10 pitch dimensions.
"""
import re
import logging
from typing import Dict, Any, List

from core.feature_extractor import FeatureExtractor

logger = logging.getLogger("PitchLens.SectionDetector")


class SectionDetector:
    """Detects section status (PRESENT, PARTIALLY_PRESENT, MISSING) and identifies missing details."""

    SECTION_KEYS = [
        "problem_clarity",
        "solution_strength",
        "market_opportunity",
        "value_proposition",
        "business_model",
        "competitive_advantage",
        "traction_validation",
        "team_execution",
        "scalability",
        "presentation_quality",
    ]

    @classmethod
    def detect_sections(cls, text: str, features: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Analyze pitch text and feature dictionary to evaluate section presence & missing sub-elements.
        Returns a dictionary mapping section keys to analysis objects:
        {
            "status": "PRESENT" | "PARTIALLY_PRESENT" | "MISSING",
            "reason": str,
            "missing_elements": List[str],
            "detected_evidence": str
        }
        """
        results = {}
        flags = features.get("presence_flags", {})
        quant = features.get("quantitative_evidence", {})

        text_lower = text.lower()

        # 1. Problem Clarity
        has_prob = flags.get("problem_present", False)
        has_prob_quant = any(k in text_lower for k in ["waste", "$", "%", "hours", "annually", "costly", "loss"])
        prob_missing = []
        if not has_prob:
            prob_status = "MISSING"
            prob_reason = "No explicit problem statement or customer pain point detected."
            prob_missing = ["Core problem description", "Target user pain points", "Problem scale/impact metrics"]
        elif not has_prob_quant:
            prob_status = "PARTIALLY_PRESENT"
            prob_reason = "Problem is mentioned conceptually, but lacks quantitative proof or cost impact metrics."
            prob_missing = ["Quantitative proof of problem scale", "Financial/time cost to customer"]
        else:
            prob_status = "PRESENT"
            prob_reason = "Problem is clearly described with specific customer impact details."

        results["problem_clarity"] = {
            "status": prob_status,
            "reason": prob_reason,
            "missing_elements": prob_missing,
        }

        # 2. Solution Strength
        has_sol = flags.get("solution_present", False)
        has_tech = flags.get("technology_present", False) or flags.get("prototype_present", False)
        sol_missing = []
        if not has_sol:
            sol_status = "MISSING"
            sol_reason = "No clear product or solution description found."
            sol_missing = ["Product/Solution overview", "Core feature mechanism", "Technology approach"]
        elif not has_tech:
            sol_status = "PARTIALLY_PRESENT"
            sol_reason = "Solution is described, but technical approach or product mechanism is sparse."
            sol_missing = ["Technical architecture / product mechanism", "Prototype / MVP status"]
        else:
            sol_status = "PRESENT"
            sol_reason = "Solution and technical mechanism are clearly articulated."

        results["solution_strength"] = {
            "status": sol_status,
            "reason": sol_reason,
            "missing_elements": sol_missing,
        }

        # 3. Market Opportunity
        has_mkt = flags.get("market_present", False)
        has_mkt_size = any(k in text_lower for k in ["tam", "sam", "som", "billion", "million", "market size", "$"])
        mkt_missing = []
        if not has_mkt:
            mkt_status = "MISSING"
            mkt_reason = "No target market or industry opportunity discussed."
            mkt_missing = ["Target customer segment", "TAM/SAM/SOM market size estimates", "Market growth drivers"]
        elif not has_mkt_size:
            mkt_status = "PARTIALLY_PRESENT"
            mkt_reason = "Target audience is mentioned, but TAM/SAM/SOM financial estimates are missing."
            mkt_missing = ["TAM/SAM/SOM market sizing", "Addressable customer volume"]
        else:
            mkt_status = "PRESENT"
            mkt_reason = "Target market and addressable size are defined with numerical estimates."

        results["market_opportunity"] = {
            "status": mkt_status,
            "reason": mkt_reason,
            "missing_elements": mkt_missing,
        }

        # 4. Value Proposition
        has_cust = flags.get("customer_present", False)
        has_usp = flags.get("usp_present", False) or "saving" in text_lower or "boost" in text_lower or "10x" in text_lower
        vp_missing = []
        if not (has_cust or has_usp):
            vp_status = "MISSING"
            vp_reason = "Value proposition and primary customer benefits are missing."
            vp_missing = ["Core benefit proposition", "Quantified customer ROI", "Primary customer use case"]
        elif not has_usp:
            vp_status = "PARTIALLY_PRESENT"
            vp_reason = "Value proposition states benefits, but lacks clear ROI quantification or unique hook."
            vp_missing = ["Quantified ROI / cost savings multiplier", "Unique value hook"]
        else:
            vp_status = "PRESENT"
            vp_reason = "Clear value proposition detailing customer benefits and specific impact."

        results["value_proposition"] = {
            "status": vp_status,
            "reason": vp_reason,
            "missing_elements": vp_missing,
        }

        # 5. Business Model
        has_bm = flags.get("business_model_present", False) or flags.get("revenue_present", False)
        has_pricing = flags.get("pricing_present", False) or any(k in text_lower for k in ["$", "₹", "fee", "per month", "per year", "commission", "margin"])
        bm_missing = []
        if not has_bm:
            bm_status = "MISSING"
            bm_reason = "Business model and monetization strategy are not explained."
            bm_missing = ["Monetization model (SaaS, transactional, licensing)", "Specific pricing numbers", "Customer payment structure"]
        elif not has_pricing:
            bm_status = "PARTIALLY_PRESENT"
            bm_reason = "Monetization model is mentioned, but specific pricing details or margins are missing."
            bm_missing = ["Specific price points", "Payment terms & frequency", "Gross/Net margin details"]
        else:
            bm_status = "PRESENT"
            bm_reason = "Business model and pricing structure are clearly specified."

        results["business_model"] = {
            "status": bm_status,
            "reason": bm_reason,
            "missing_elements": bm_missing,
        }

        # 6. Competitive Advantage
        has_comp = flags.get("competition_present", False)
        has_moat = flags.get("usp_present", False) or any(k in text_lower for k in ["unlike", "versus", "vs", "advantage", "patent", "faster", "cheaper"])
        comp_missing = []
        if not has_comp:
            comp_status = "MISSING"
            comp_reason = "Competitive landscape and alternative solutions are not addressed."
            comp_missing = ["Existing competitors list", "Key differentiators / defensibility", "Competitive positioning"]
        elif not has_moat:
            comp_status = "PARTIALLY_PRESENT"
            comp_reason = "Competitors are named, but unfair competitive advantage or moat is unclear."
            comp_missing = ["Defensible moat / proprietary edge", "Direct feature-by-feature differentiation"]
        else:
            comp_status = "PRESENT"
            comp_reason = "Competitors and distinct competitive advantages are clearly identified."

        results["competitive_advantage"] = {
            "status": comp_status,
            "reason": comp_reason,
            "missing_elements": comp_missing,
        }

        # 7. Traction & Validation
        has_trac = flags.get("traction_present", False)
        has_quant_trac = quant.get("has_quantitative_evidence", False)
        trac_missing = []
        if not has_trac:
            trac_status = "MISSING"
            trac_reason = "No evidence of customer traction, pilots, or product validation."
            trac_missing = ["User/Customer numbers", "Revenue / MRR / ARR metrics", "Pilot results or customer testimonials"]
        elif not has_quant_trac:
            trac_status = "PARTIALLY_PRESENT"
            trac_reason = "Traction is mentioned qualitatively, but quantitative proof (revenue, users, growth %) is absent."
            trac_missing = ["Specific user/customer metrics", "Verified revenue or pilot metrics"]
        else:
            trac_status = "PRESENT"
            trac_reason = "Strong quantitative traction evidence detected with numerical metrics."

        results["traction_validation"] = {
            "status": trac_status,
            "reason": trac_reason,
            "missing_elements": trac_missing,
        }

        # 8. Team & Execution
        has_team = flags.get("team_present", False)
        has_exp = any(k in text_lower for k in ["ex-", "alumni", "years", "phd", "md", "engineer", "founder", "veteran", "senior", "experience", "stanford", "harvard", "mit"])
        team_missing = []
        if not has_team:
            team_status = "MISSING"
            team_reason = "Founding team members and relevant expertise are not mentioned."
            team_missing = ["Founder backgrounds", "Relevant industry expertise", "Technical / domain leadership"]
        elif not has_exp:
            team_status = "PARTIALLY_PRESENT"
            team_reason = "Team is mentioned, but specific prior background, track record, or credentials are sparse."
            team_missing = ["Prior industry track record", "Key domain credentials / degrees"]
        else:
            team_status = "PRESENT"
            team_reason = "Team credentials and relevant domain experience are clearly established."

        results["team_execution"] = {
            "status": team_status,
            "reason": team_reason,
            "missing_elements": team_missing,
        }

        # 9. Scalability
        has_scale = flags.get("scalability_present", False) or flags.get("roadmap_present", False) or any(k in text_lower for k in ["scale", "architecture", "distributed", "cloud", "expansion", "automation", "depot"])
        scale_missing = []
        if not has_scale:
            scale_status = "MISSING"
            scale_reason = "Scalability model and future growth vision are not addressed."
            scale_missing = ["Scalable architecture / operations", "Geographic or sector expansion plan", "Unit economics scaling model"]
        elif "scale" not in text_lower and "architecture" not in text_lower:
            scale_status = "PARTIALLY_PRESENT"
            scale_reason = "Growth goals are stated, but technical or operational scalability mechanics are light."
            scale_missing = ["Operational / technical scaling mechanism"]
        else:
            scale_status = "PRESENT"
            scale_reason = "Scalability approach and growth vision are clearly articulated."

        results["scalability"] = {
            "status": scale_status,
            "reason": scale_reason,
            "missing_elements": scale_missing,
        }

        # 10. Presentation Quality
        word_cnt = len(text.split())
        sent_cnt = len(re.split(r"[.!?]", text))
        avg_len = word_cnt / max(sent_cnt, 1)

        pres_missing = []
        if word_cnt < 40:
            pres_status = "MISSING"
            pres_reason = "Pitch is extremely brief (<40 words) and lacks sufficient detail for full evaluation."
            pres_missing = ["Comprehensive narrative", "Detailed section descriptions"]
        elif word_cnt < 80 or avg_len > 45:
            pres_status = "PARTIALLY_PRESENT"
            pres_reason = "Pitch text is short (<80 words) or contains overly complex sentences."
            pres_missing = ["Sufficient narrative depth", "Balanced sentence structure"]
        else:
            pres_status = "PRESENT"
            pres_reason = "Pitch is well-structured with clear professional presentation."

        results["presentation_quality"] = {
            "status": pres_status,
            "reason": pres_reason,
            "missing_elements": pres_missing,
        }

        return results
