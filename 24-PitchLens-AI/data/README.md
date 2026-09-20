# PitchLens AI - Data Directory

This directory contains baseline datasets used for feature similarity benchmarking and ML model training.

## Files

1. `successful_pitches.csv`: Synthetic dataset containing pitch examples across multiple industries.
   - **IMPORTANT DISCLAIMER**: This dataset contains **DEMO / SYNTHETIC DATA** created for testing and demonstration purposes. It does not represent actual confidential startup data, nor should predictions derived from it be interpreted as real-world financial or investment advice.

2. `sample_pitches.csv`: Ready-to-use sample pitches for quick testing within the PitchLens AI desktop user interface:
   - **Strong Pitch (SaaS)**: Complete pitch with strong quantitative traction and revenue model.
   - **Weak Pitch**: Sparse pitch missing business model, competition, and traction.
   - **Solution-Heavy Pitch**: Deep technical solution but missing clear monetization and pricing.
   - **Traction-Heavy Pitch**: Strong user/revenue numbers but lacking competitive landscape analysis.
   - **Missing Market Pitch**: Clear problem/solution but missing TAM/SAM/SOM target market details.

## CSV Schema for `successful_pitches.csv`

| Column | Description |
|---|---|
| `id` | Unique pitch identifier |
| `pitch_name` | Title of the pitch |
| `industry` | Business sector (SaaS, FinTech, HealthTech, etc.) |
| `pitch_text` | Complete pitch narrative text |
| `problem` | Stated problem summary |
| `solution` | Stated solution summary |
| `market` | Target market details |
| `business_model` | Monetization & pricing model |
| `traction` | Key metrics, revenue, users, or pilots |
| `competition` | Competitors and differentiation |
| `team` | Team background & expertise |
| `scalability` | Scalability & growth vision |
| `presentation_quality` | Structure & clarity rating (1-100) |
| `success_label` | Binary classification (1 = Strong Benchmark, 0 = Needs Development) |
