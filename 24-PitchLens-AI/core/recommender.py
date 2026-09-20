"""
Recommender Engine Module for PitchLens AI
Generates actionable, prioritized pitch recommendations, strengths, weaknesses, and missing elements.
"""
import logging
from typing import Dict, Any, List

from config.settings import CATEGORY_DISPLAY_NAMES

logger = logging.getLogger("PitchLens.RecommenderEngine")


class RecommenderEngine:
    """Derives actionable recommendations and strengths/weaknesses from evaluation signals."""

    # Recommendation templates mapped to categories
    RECOMMENDATION_TEMPLATES = {
        "business_model": {
            "title": "Specify Pricing Structure and Monetization Details",
            "problem": "The pitch lacks concrete pricing points, customer payment frequency, or gross margin details.",
            "why_it_matters": "Investors require clear unit economics to evaluate profitability, customer acquisition feasibility, and scalable business viability.",
            "what_to_add": "Specify exact price points (e.g. $499/mo per seat), payment terms (annual/monthly subscription, transactional fee), customer payment mechanics, and gross margin estimates.",
            "suggested_questions": [
                "Who pays for the product and what is the exact price?",
                "Is the revenue model subscription, pay-per-use, or transaction fee?",
                "What are your projected gross margins?"
            ]
        },
        "competitive_advantage": {
            "title": "Define Competitive Landscape and Defensible Moat",
            "problem": "Existing competitors or key product differentiation are not explicitly articulated.",
            "why_it_matters": "Without explicit competitive positioning, reviewers cannot judge defensibility or why customers would choose your solution over alternatives.",
            "what_to_add": "Identify key incumbent competitors and alternative workarounds. Explicitly list 2-3 unique defensible advantages (e.g., 10x faster execution, proprietary patent, native workflow integration).",
            "suggested_questions": [
                "Who are your top 3 direct and indirect competitors?",
                "What is your unfair advantage or proprietary tech moat?",
                "Why will customers switch from their current workflow?"
            ]
        },
        "traction_validation": {
            "title": "Add Quantitative Traction and Customer Proof",
            "problem": "The pitch lacks verified quantitative proof such as active users, pilot metrics, or recurring revenue figures.",
            "why_it_matters": "Quantitative traction is the strongest evidence of market demand and reduces execution risk for investors.",
            "what_to_add": "Include quantitative metrics such as active user counts, pilot trial numbers, MRR/ARR growth, customer retention rates, or user satisfaction scores.",
            "suggested_questions": [
                "How many active users, pilot accounts, or paying clients do you currently have?",
                "What is your current Monthly Recurring Revenue (MRR) or contract pipeline?",
                "What quantitative metrics demonstrate customer retention or satisfaction?"
            ]
        },
        "market_opportunity": {
            "title": "Provide TAM / SAM / SOM Market Sizing",
            "problem": "Target market size is presented vaguely without numerical addressable market calculations.",
            "why_it_matters": "Investors need to verify that the market is large enough to support a high-growth scalable business.",
            "what_to_add": "Provide top-down or bottom-up estimates for Total Addressable Market (TAM), Serviceable Addressable Market (SAM), and Serviceable Obtainable Market (SOM).",
            "suggested_questions": [
                "What is the total dollar value of your TAM, SAM, and SOM?",
                "How many potential target customers exist in your initial beachhead segment?",
                "What key macro trends are driving market growth?"
            ]
        },
        "problem_clarity": {
            "title": "Quantify Problem Scale and Customer Pain",
            "problem": "The problem is described abstractly without metrics showing financial or operational impact.",
            "why_it_matters": "A clearly quantified problem creates urgency and validates why customers will pay for a solution.",
            "what_to_add": "Add metrics demonstrating the scale of the pain (e.g., $30B annual waste, 3 hours lost daily, 24% error rate).",
            "suggested_questions": [
                "How much time or money do target customers lose due to this problem?",
                "How many businesses or individuals suffer from this issue daily?",
                "Why is existing status quo painful enough to force change?"
            ]
        },
        "team_execution": {
            "title": "Highlight Founder Track Record and Domain Expertise",
            "problem": "Founding team members, credentials, and relevant domain track records are missing.",
            "why_it_matters": "Early-stage evaluation heavily weighs the founding team's capability to execute the plan.",
            "what_to_add": "Mention key founders, prior industry roles (e.g. ex-Google, ex-AWS, PhD), technical accomplishments, or domain authority.",
            "suggested_questions": [
                "Who are the core founders and what are their relevant backgrounds?",
                "What unique domain expertise or technical accomplishments does the team possess?",
                "Have team members previously built or scaled similar technology?"
            ]
        },
        "solution_strength": {
            "title": "Clarify Solution Mechanism and Product Architecture",
            "problem": "The solution is stated conceptually without explaining how the technology actually operates.",
            "why_it_matters": "Reviewers must understand the product mechanism to verify technical feasibility.",
            "what_to_add": "Explain the core product workflow, underlying technology engine (AI, IoT, cloud microservices), and current prototype state.",
            "suggested_questions": [
                "How does the core product actually work step-by-step?",
                "What proprietary technology or platform architecture powers the solution?",
                "What is the current development stage (concept, prototype, MVP, production)?"
            ]
        },
        "value_proposition": {
            "title": "Articulate Quantified Customer ROI",
            "problem": "Primary customer value proposition lacks clear cost/time savings multiplier.",
            "why_it_matters": "Customers buy based on clear economic ROI or compelling benefit multipliers.",
            "what_to_add": "Include explicit ROI metrics (e.g. 10x faster execution, 20% cost reduction, 42% time savings).",
            "suggested_questions": [
                "What exact ROI multiplier or cost reduction does the customer achieve?",
                "What is the single most compelling reason a customer buys your product?"
            ]
        },
        "scalability": {
            "title": "Detail Scalability and Operational Expansion Model",
            "problem": "Long-term scalability mechanics or expansion plans are not outlined.",
            "why_it_matters": "Venture-scale returns require a business model that scales non-linearly with lower incremental costs.",
            "what_to_add": "Describe technical architecture scalability (serverless, cloud APIs) or operational leverage models.",
            "suggested_questions": [
                "How will software or operations scale without linear cost increases?",
                "What is your geographic or product line expansion roadmap?"
            ]
        },
        "presentation_quality": {
            "title": "Enhance Pitch Narrative Structure and Specificity",
            "problem": "The narrative is too brief or lacks structured presentation depth.",
            "why_it_matters": "Professional, clear pitch structure improves credibility and investor engagement.",
            "what_to_add": "Expand sparse sections with concrete data, clear paragraph structure, and executive precision.",
            "suggested_questions": [
                "Is every major pitch section clearly demarcated?",
                "Are all claims backed by specific figures rather than generic buzzwords?"
            ]
        }
    }

    @classmethod
    def generate_recommendations(
        self,
        category_scores: Dict[str, float],
        section_analysis: Dict[str, Dict[str, Any]],
        features: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Derive prioritized actionable recommendations (HIGH, MEDIUM, LOW priority).
        """
        recommendations = []

        # Sort categories by lowest score first
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1])

        for cat_key, score in sorted_categories:
            status = section_analysis.get(cat_key, {}).get("status", "MISSING")

            # Determine priority
            if status == "MISSING" or score < 45:
                priority = "HIGH"
            elif status == "PARTIALLY_PRESENT" or score < 70:
                priority = "MEDIUM"
            else:
                priority = "LOW"

            # Skip LOW priority if we already have sufficient higher priority recommendations
            if priority == "LOW" and len(recommendations) >= 4:
                continue

            template = self.RECOMMENDATION_TEMPLATES.get(cat_key, {
                "title": f"Improve {CATEGORY_DISPLAY_NAMES.get(cat_key, cat_key)}",
                "problem": f"The {cat_key} section scored {score}/100.",
                "why_it_matters": "Completeness in this area improves overall pitch strength.",
                "what_to_add": f"Add detailed information regarding {cat_key}.",
                "suggested_questions": [f"What additional details can be added for {cat_key}?"]
            })

            rec_item = {
                "category": cat_key,
                "priority": priority,
                "title": template["title"],
                "problem": template["problem"],
                "why_it_matters": template["why_it_matters"],
                "what_to_add": template["what_to_add"],
                "suggested_questions": " | ".join(template["suggested_questions"])
            }
            recommendations.append(rec_item)

        return recommendations[:6]  # Return top 6 actionable recommendations

    @classmethod
    def extract_strengths(cls, section_analysis: Dict[str, Dict[str, Any]], features: Dict[str, Any]) -> List[str]:
        """Extract automated, evidence-backed strength statements."""
        strengths = []
        quant = features.get("quantitative_evidence", {})

        for cat_key, analysis in section_analysis.items():
            display_name = CATEGORY_DISPLAY_NAMES.get(cat_key, cat_key)
            if analysis["status"] == "PRESENT":
                if cat_key == "problem_clarity":
                    strengths.append("Problem is clearly defined with specific target pain points.")
                elif cat_key == "solution_strength":
                    strengths.append("Solution and product implementation mechanism are explicitly articulated.")
                elif cat_key == "business_model":
                    strengths.append("Business monetization model and pricing structure are clearly specified.")
                elif cat_key == "competitive_advantage":
                    strengths.append("Competitive differentiation and market defensibility are addressed.")
                elif cat_key == "traction_validation":
                    strengths.append("Strong validation evidence detected with customer/revenue traction.")
                elif cat_key == "team_execution":
                    strengths.append("Founding team background and relevant domain expertise are established.")
                elif cat_key == "market_opportunity":
                    strengths.append("Target market opportunity and addressable audience are clearly identified.")
                else:
                    strengths.append(f"{display_name} section is thoroughly developed.")

        if quant.get("has_quantitative_evidence", False):
            strengths.append("Pitch includes strong quantitative metrics (currencies, percentages, user numbers).")

        if not strengths:
            strengths.append("Basic pitch structure present.")

        return strengths[:5]

    @classmethod
    def extract_weaknesses(cls, section_analysis: Dict[str, Dict[str, Any]], features: Dict[str, Any]) -> List[str]:
        """Extract automated weakness statements based on missing/partial sections."""
        weaknesses = []
        quant = features.get("quantitative_evidence", {})

        for cat_key, analysis in section_analysis.items():
            status = analysis["status"]
            display_name = CATEGORY_DISPLAY_NAMES.get(cat_key, cat_key)
            reason = analysis.get("reason", "")
            if status == "MISSING":
                weaknesses.append(f"{display_name} section is missing from the pitch.")
            elif status == "PARTIALLY_PRESENT":
                weaknesses.append(f"{display_name} is partially described but lacks detail: {reason}")

        if not quant.get("has_quantitative_evidence", False):
            weaknesses.append("No quantitative validation metrics (revenue, users, growth %) were detected.")

        if not weaknesses:
            weaknesses.append("Minor improvements possible in section formatting.")

        return weaknesses[:5]

    @classmethod
    def extract_missing_elements(cls, section_analysis: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
        """Categorize missing sub-elements by priority (HIGH, MEDIUM)."""
        missing_by_priority = {"HIGH": [], "MEDIUM": []}

        for cat_key, analysis in section_analysis.items():
            status = analysis["status"]
            elements = analysis.get("missing_elements", [])
            display_name = CATEGORY_DISPLAY_NAMES.get(cat_key, cat_key)

            for el in elements:
                item_str = f"{display_name}: {el}"
                if status == "MISSING":
                    missing_by_priority["HIGH"].append(item_str)
                elif status == "PARTIALLY_PRESENT":
                    missing_by_priority["MEDIUM"].append(item_str)

        return missing_by_priority
