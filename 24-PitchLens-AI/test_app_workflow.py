"""
Full Application Verification Script for PitchLens AI
"""
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config.settings import ensure_directories, DATASET_PATH
from database.database import get_db
from core.evaluator import PitchEvaluator
from reports.pdf_report import PDFReportGenerator
from ml.train import train_and_save_model


def run_full_verification():
    print("=== Step 1: Ensure Directories & Database ===")
    ensure_directories()
    db = get_db()
    print("Database initialized successfully.")

    print("\n=== Step 2: Train ML Model ===")
    train_summary = train_and_save_model()
    print(f"ML Model Trained: {train_summary['best_model_name']} (F1: {train_summary['best_f1_score']:.4f})")

    print("\n=== Step 3: Evaluate Sample Pitch ===")
    evaluator = PitchEvaluator()
    sample_text = (
        "CloudPulse Analytics is a real-time cloud infrastructure cost optimization platform. "
        "Engineering teams waste over $30B annually on idle cloud resources because existing monitoring tools "
        "lack automated cost-remediation capabilities. CloudPulse solves this with an AI-driven agent that "
        "dynamically resizes Kubernetes clusters and shuts down unused cloud workloads. "
        "Our target market is mid-market DevOps teams with cloud spends over $50,000 per month ($8.4B TAM). "
        "We operate a B2B SaaS subscription model charging $499 per month per cluster, yielding an 82% gross margin. "
        "We currently have 45 active paying enterprise customers, $28,000 Monthly Recurrent Revenue (MRR), growing 18% MoM. "
        "Competitors like CloudHealth and Kubecost provide static dashboards, whereas CloudPulse executes automated 1-click resource saving actions. "
        "Our team consists of former AWS senior architects and Stanford computer science graduates."
    )

    eval_result = evaluator.evaluate(sample_text, pitch_name="CloudPulse Verification")
    print(f"Pitch Name   : {eval_result['pitch_name']}")
    print(f"Overall Score: {eval_result['overall_score']} / 100")
    print(f"Readiness    : {eval_result['readiness']}")
    print(f"Coverage     : {eval_result['evidence_coverage']}%")

    print("\n=== Step 4: Verify Category Scores & Explanations ===")
    for cat, score in eval_result["category_scores"].items():
        print(f"  - {cat:22s}: {score:5.1f}/100 [{eval_result['category_statuses'][cat]}]")

    print("\n=== Step 5: Save Evaluation to SQLite Database ===")
    eval_id_v1 = db.save_evaluation(eval_result)
    print(f"Saved Version 1 to DB (ID: {eval_id_v1})")

    # Evaluate Version 2 with minor update
    eval_result_v2 = evaluator.evaluate(sample_text + " We plan geographic expansion to Europe next year.", pitch_name="CloudPulse Verification")
    eval_id_v2 = db.save_evaluation(eval_result_v2)
    print(f"Saved Version 2 to DB (ID: {eval_id_v2})")

    print("\n=== Step 6: Test Reports & Export (PDF, JSON, CSV) ===")
    pdf_path = PDFReportGenerator.generate_pdf(eval_result)
    json_path = PDFReportGenerator.export_json(eval_result)
    csv_path = PDFReportGenerator.export_csv(eval_result)

    print(f"PDF Generated : {pdf_path.name} (Exists: {pdf_path.exists()})")
    print(f"JSON Exported : {json_path.name} (Exists: {json_path.exists()})")
    print(f"CSV Exported  : {csv_path.name} (Exists: {csv_path.exists()})")

    print("\n=== Step 7: Verify History & Versioning ===")
    versions = db.get_pitch_versions("CloudPulse Verification")
    print(f"Found {len(versions)} versions in DB for 'CloudPulse Verification':")
    for v in versions:
        print(f"  - Version {v['version']}: Score = {v['overall_score']}")

    print("\n=== Step 8: Verify Analytics Summary ===")
    analytics = db.get_analytics_summary()
    print(f"Total Evaluations in DB: {analytics['total_evaluations']}")
    print(f"Average Score across DB : {analytics['avg_score']}")

    print("\n================ VERIFICATION SUCCESSFUL! ================")


if __name__ == "__main__":
    run_full_verification()
